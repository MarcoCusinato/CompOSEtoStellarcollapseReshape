import numpy as np
from src.CompOSE_periodic_table.periodic_table import periodic_table



def detect_muons(eosinfo):
    """
    Detects if muons are present in the EOS. If so, EOS cannot be converted to stellarcollapse format,
    because charge fraction is not equal to the electron fraction.
    """
    for key in eosinfo:
        if eosinfo[key]["type"] != "particle":
            continue
        index = eosinfo[key]["index"]
        if type(index) == str:
            continue
        try:
            name = periodic_table(index)["name"]
        except:
            continue
        if name == "muon":
            raise ValueError("Muons detected, cannot convert this EOS from CompOSE to stellarcollapse.")

def read_TrhoYe(EOS_CompOSE, eosinfo, quantities_out, conv):
    """
    Reads the temperature, density, and electron fraction points from the CompOSE EOS.
    Saves into a dictionary together with the number of points in each dimension.
    """
    print("Reading temperature, density, and electron fraction points from EOS...")
    detect_muons(eosinfo)
    try:
        quantities_out['logrho'] = np.log10(conv.mass_density(EOS_CompOSE['Parameters']['nb'][...].astype(float)))
        quantities_out['pointsrho'] = quantities_out['logrho'].shape[0]
    except:
        raise ValueError("No density points found in EOS.")
    try:
        quantities_out['logtemp'] = np.log10(EOS_CompOSE['Parameters']['t'][...].astype(float))
        quantities_out['pointstemp'] = quantities_out['logtemp'].shape[0]
    except:
        raise ValueError("No temperature points found in EOS.")
    try:
        quantities_out['ye'] = EOS_CompOSE['Parameters']['yq'][...].astype(float)
        quantities_out['pointsye'] = quantities_out['ye'].shape[0]
    except:
        raise ValueError("No electron fraction points found in EOS.")
    print("Done.")
    return quantities_out
    