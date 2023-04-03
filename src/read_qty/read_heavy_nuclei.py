import numpy as np
from src.CompOSE_periodic_table.periodic_table import periodic_table
import warnings

def read_heavy_nuclei(EOS_CompOSE, eosinfo, quantities_out, error):
    """
    Reads the average mass and charge of the heavy nuclei from the CompOSE EOS
    amd calculates their average mass fraction.
    """
    print("Reading heavy nuclei compositio from EOS...")
    print("Stellarcollapse assumes that the lower number for the heavy nuclei average mass and charge is the one, while " +\
          "CompOSE assumes that is 0. Setting all numbers lower than 1 to 1.")
    heavy_nuclei_indices = EOS_CompOSE['Composition_quadrupels']['index_av'][...]
    
    if heavy_nuclei_indices.size == 0:
        raise ValueError("No heavy nuclei found in EOS.")
    
    elif heavy_nuclei_indices.size == 1:
        quantities_out['Abar'] = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['aav'][0, ...])).astype(float)
        yh = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['yav'][0, ...])).astype(float)
        if yh.min() < 0:
            warnings.warn("The mass fraction of heavy nuclei is negative. It will be set to zero.")
            error = True
            yh = np.where(yh < 0, 0, yh)
        quantities_out['Abar'] = np.where(quantities_out['Abar'] < 1, 1, quantities_out['Abar'])
        quantities_out['Zbar'] = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['zav'][0, ...])).astype(float)
        quantities_out['Zbar'] = np.where(quantities_out['Zbar'] < 1, 1, quantities_out['Zbar']).astype(float)
        quantities_out['Xh'] = quantities_out['Abar'] * yh
        del yh
    elif heavy_nuclei_indices.size == 2:
        print("Warning, more than one heavy nuclei index found. Assuming that one represents nuclei with " + \
              r"$2\leq A < 20$ and the other represents nuclei with $A \geq 20$.\n" + \
              "Since usually heavy nuclei are the ones with $A > 4$, we will manipulate the fractions to make it so.\n" + \
              "Please make sure that all the nuclei with $A <= 4$ have been saved in the EOS.")
        print("This method would apply some corrections to Abar, yh and Zbar (read the README for further info).")
        composition_pairs_indices = EOS_CompOSE['Composition_pairs']['index_yi'][...]
        index2, index20 = 0, 1
        ## Loading the data
        Abar2 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['aav'][index2, ...])).astype(float)
        if Abar2.max() > 20:
            index2, index20 = 1, 0
            Abar20, Abar2 = Abar2, (np.squeeze(EOS_CompOSE['Composition_quadrupels']['aav'][index2, ...])).astype(float)
        else:
            Abar20 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['aav'][index20, ...])).astype(float)
        
        ## Load Z, y for 2 and 20 nuclei
        yh2 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['yav'][index2, ...])).astype(float)
        yh20 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['yav'][index20, ...])).astype(float)
        Zbar2 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['zav'][index2, ...])).astype(float)
        Zbar20 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['zav'][index20, ...])).astype(float)
        ## Check the data and apply corrections if needed.
        ## A2: 0 where Abar < 2 or Zbar < 1 or y < 0
        ## y2: 0 where Abar == 0 or y < 0
        ## Z2: 0 where Abar == 0
        ## A20: 0 where Abar < 20
        ## y20: 0 where Abar < 20 or y < 0
        ## Z20: 0 where Abar < 20

        Abar2 = np.where((Abar2 < 2) | (Zbar2 < 1) | (yh2 < 0), 0, Abar2)
        yh2 = np.where((Abar2 == 0) | (yh2 < 0), 0, yh2)
        Zbar2 = np.where(Abar2 == 0, 0, Zbar2)
        Abar20 = np.where((Abar20 < 20) | (Zbar20 < 1) | (yh20 < 0), 0, Abar20)
        yh20 = np.where((Abar20 < 20) | (yh20 < 0), 0, yh20)
        Zbar20 = np.where(Abar20 < 20, 0, Zbar20)

        ## Checking the particles with 2 <= A <= 4 and storing their ye, A and Z
        ylight, Alight, Zlight = 0, 0, 0
        for key in eosinfo:
            if eosinfo[key]["type"] != "particle":
                continue
            particle_index = eosinfo[key]["index"]
            particle_info = periodic_table(particle_index)
            if particle_info["A"] >= 2 and particle_info["A"] <= 4:
                index = np.where(composition_pairs_indices == particle_index)[0]
                yindex = np.squeeze(EOS_CompOSE['Composition_pairs']['yi'][index, ...]).astype(float)
                yindex = np.where((yindex < 0) | (Abar2 == 0), 0, yindex)
                ylight += yindex
                Alight += particle_info["A"] * yindex
                Zlight += particle_info["Z"] * yindex
        with np.errstate(all='ignore'):   
            Alight = np.nan_to_num(Alight / ylight)
            Zlight = np.nan_to_num(Zlight / ylight)
            yden = np.where((yh2 - ylight) < 0, 0, (yh2 - ylight))
            Abar2 = (Abar2 * yh2 - Alight) / (yden)
            Abar2 = np.nan_to_num(Abar2)
            Zbar2 = (Zbar2 * yh2 - Zlight) / (yden)
            Zbar2 = np.nan_to_num(Zbar2)
            yh2 = yden
            quantities_out['Abar'] = (Abar2 * yh2 + Abar20 * yh20) / (yh2 + yh20)
            quantities_out['Zbar'] = (Zbar2 * yh2 + Zbar20 * yh20) / (yh2 + yh20)

        quantities_out['Abar'] = np.nan_to_num(quantities_out['Abar'])
        quantities_out['Abar'] = np.where(quantities_out['Abar'] < 1, 1, quantities_out['Abar'])
        quantities_out['Zbar'] = np.nan_to_num(quantities_out['Zbar'])
        quantities_out['Zbar'] = np.where(quantities_out['Zbar'] < 1, 1, quantities_out['Zbar'])
        quantities_out['Xh'] = quantities_out['Abar'] * (yh2 + yh20)
        del yh2, yh20, Zbar2, Zbar20, Abar2, Abar20, ylight, Alight, Zlight, yden
        Zbar2 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['zav'][index2, ...])).astype(float)
        yh2 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['yav'][index2, ...])).astype(float)
        Zbar20 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['zav'][index20, ...])).astype(float)
        yh20 = (np.squeeze(EOS_CompOSE['Composition_quadrupels']['yav'][index20, ...])).astype(float)
    else:
        raise ValueError("More than two heavy nuclei found in EOS.\n" + \
                         "Please send me the EOS you are trying to use so I can add support for it.")
        
    print("Done.")
    return quantities_out, error