
from rdkit import Chem
import numpy as np
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed, TimeoutError

from tqdm import tqdm
import osmordred as rd




# Define descriptor computation function
def CalcOsmordred(smiles, version=2, names = False, mynames=[]):


    if version == 1:
        " original version from Mordred"
        v = 1
        doExEstate = False
    else:
        " expended descriptors with more features and fixed InformationContent in cpp"
        v = 2
        doExEstate = True

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None # Return an empty array instead of None

    results = []
    descriptor_names = []

    # Define descriptors with names
    descriptors = [
        ("ABCIndex", rd.CalcABCIndex),
        ("AcidBase", rd.CalcAcidBase),
        ("AdjacencyMatrix", lambda mol: rd.CalcAdjacencyMatrix(mol, v)),
        ("Aromatic", rd.CalcAromatic),
        ("AtomCount", lambda mol: rd.CalcAtomCount(mol, v)),
        ("Autocorrelation", rd.CalcAutocorrelation),
        ("BCUT", rd.CalcBCUT),
        ("BalabanJ", rd.CalcBalabanJ),
        ("BaryszMatrix", rd.CalcBaryszMatrix),
        ("BertzCT", rd.CalcBertzCT),
        ("BondCount", rd.CalcBondCount),
        ("RNCGRPCG", rd.CalcRNCGRPCG),
        ("CarbonTypes", lambda mol: rd.CalcCarbonTypes(mol, v)),
        ("Chi", rd.CalcChi),
        ("Constitutional", rd.CalcConstitutional),
        ("DetourMatrix", rd.CalcDetourMatrix),
        ("DistanceMatrix", lambda mol: rd.CalcDistanceMatrix(mol, v)),
        ("EState", lambda mol: rd.CalcEState(mol, doExEstate)),
        ("EccentricConnectivityIndex", rd.CalcEccentricConnectivityIndex),
        ("ExtendedTopochemicalAtom", rd.CalcExtendedTopochemicalAtom),
        ("FragmentComplexity", rd.CalcFragmentComplexity),
        ("Framework", rd.CalcFramework),
        ("HydrogenBond", rd.CalcHydrogenBond),
    ]

    if version == 1:
        descriptors.append(("InformationContentv1", CalcIC))
    else:
        descriptors.append(("LogS", rd.CalcLogS))
        descriptors.append(("InformationContentv2", lambda mol: rd.CalcInformationContent(mol, 5)))

    additional_descriptors = [
        ("KappaShapeIndex", rd.CalcKappaShapeIndex),
        ("Lipinski", rd.CalcLipinski),
        ("McGowanVolume", rd.CalcMcGowanVolume),
        ("MoeType", rd.CalcMoeType),
        ("MolecularDistanceEdge", rd.CalcMolecularDistanceEdge),
        ("MolecularId", rd.CalcMolecularId),
        ("PathCount", rd.CalcPathCount),
        ("Polarizability", rd.CalcPolarizability),
        ("RingCount", rd.CalcRingCount),
        ("RotatableBond", rd.CalcRotatableBond),
        ("SLogP", rd.CalcSLogP),
        ("TopoPSA", rd.CalcTopoPSA),
        ("TopologicalCharge", rd.CalcTopologicalCharge),
        ("TopologicalIndex", rd.CalcTopologicalIndex),
        ("VdwVolumeABC", rd.CalcVdwVolumeABC),
        ("VertexAdjacencyInformation", rd.CalcVertexAdjacencyInformation),
        ("WalkCount", rd.CalcWalkCount),
        ("Weight", rd.CalcWeight),
        ("WienerIndex", rd.CalcWienerIndex),
        ("ZagrebIndex", rd.CalcZagrebIndex),
    ]

    descriptors.extend(additional_descriptors)
    # not yet implemented ODT
    if version > 1:
        extended_descriptors = [
            ("Pol", rd.CalcPol),
            ("MR", rd.CalcMR),
            ("Flexibility", rd.CalcFlexibility),
            ("Schultz", rd.CalcSchultz),
            ("AlphaKappaShapeIndex", rd.CalcAlphaKappaShapeIndex),
            ("HEState", rd.CalcHEState),
            ("BEState", rd.CalcBEState),
            ("Abrahams", rd.CalcAbrahams),
            ("ANMat", rd.CalcANMat),
            ("ASMat", rd.CalcASMat),
            ("AZMat", rd.CalcAZMat),
            ("DSMat", rd.CalcDSMat),
            ("DN2Mat", rd.CalcDN2Mat),
            ("Frags", rd.CalcFrags),
            ("AddFeatures", rd.CalcAddFeatures),
        ]
        descriptors.extend(extended_descriptors)

    #try:
    for name, func in descriptors:
        try:
            value = func(mol)
    
            value = np.atleast_1d(np.array(value))
            results.append(value)
        except:
            arraylength =np.sum([1 for c in mynames if c.startswith(name)])
            print(name,' error for smiles ', smiles)
            
            results.append(np.full((arraylength,), np.nan))
        if names:
            descriptor_names.extend([f"{name}_{i+1}" for i in range(len(value))])
    if names:
        return np.concatenate(results), descriptor_names
    return np.concatenate(results)



if __name__ == "__main__":
    _, mynames = CalcOsmordred('CCCO',version=2, names=True)
    print(len(mynames))
    smiles = ['CCCO','CCCN','c1ccccc1']
    for s in smiles:
        mol = Chem.MolFromSmiles(s)
        results =  CalcOsmordred(s, version=2,names=False,mynames= mynames)
        print(list(results))
        
