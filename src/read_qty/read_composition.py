from src.CompOSE_periodic_table.periodic_table import periodic_table
import numpy as np
import warnings

def check_mandatory_particles(quantities_out):
    """
    Checks if the EOS contains the mandatory particles: proton, neutron, and alphas.
    """
    mandatory_particles = ["Xn", "Xp", "Xa"]
    missing_particles = []
    for particle in mandatory_particles:
        if particle not in quantities_out:
            missing_particles.append(particle)
    if len(missing_particles) > 0:
        raise ValueError("The following particles are missing: " + str(missing_particles))
    
def read_mass_fractions(EOS_CompOSE, eosinfo, quantities_out, error):
    """
    Reads the particle fractions from the CompOSE EOS and convert them
    into mass fractions.
    """
    print("Reading light nuclei from EOS...")
    composition_pairs_indices = EOS_CompOSE['Composition_pairs']['index_yi'][...]
    for key in eosinfo:
        if eosinfo[key]["type"] != "particle":
            continue
        particle_index = eosinfo[key]["index"]
        try:
            particle_info = periodic_table(particle_index)
        except:
            print("Particle index " + str(particle_index) + " not found in periodic table. Skipping.")
            continue
        if particle_info["name"] == 'e':
            continue
        
        index = np.where(composition_pairs_indices == particle_index)[0]
        if particle_info["A"] > 0:
            quantities_out["X" + particle_info["name"]] = np.squeeze(EOS_CompOSE['Composition_pairs']['yi'][index, ...]).astype(float) \
                * particle_info["A"]
            if quantities_out["X" + particle_info["name"]].min() < 0:
                warnings.warn("The mass fraction of " + particle_info["name"] + " is negative. Setting it to 0.")
                error = True
                quantities_out["X" + particle_info["name"]] = np.where(quantities_out["X" + particle_info["name"]] < 0, 0, quantities_out["X" + particle_info["name"]])
        else:
            quantities_out["y" + particle_info["name"]] = np.squeeze(EOS_CompOSE['Composition_pairs']['yi'][index, ...]).astype(float)
            if quantities_out["y" + particle_info["name"]].min() < 0:
                warnings.warn("The mass fraction of " + particle_info["name"] + " is negative. Setting it to 0.")
                error = True
                quantities_out["y" + particle_info["name"]] = np.where(quantities_out["y" + particle_info["name"]] < 0, 0, quantities_out["y" + particle_info["name"]])

    check_mandatory_particles(quantities_out)
    print("Done.")
    return quantities_out, error
