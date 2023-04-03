from src.math_functions.derivative import Derive
import numpy as np
import warnings



def check_mandatory_thermo_quantities(quantities_out, mu_q, mu_l, epsilon):
    """
    Check if all the required thermodynamic quantities are present in the EOS.
    """
    mandatory = ["logpress", "entropy", "mu_n", "logenergy", "cs2"]
    missing = []
    if mu_q is None:
        missing.append("mu_q")
    if mu_l is None:
        missing.append("mu_l")
    if epsilon is None:
        missing.append("epsilon")
    for key in mandatory:
        if key not in quantities_out:
            missing.append(key)
    if len(missing) > 0:
        raise ValueError("The following thermo quantities are missing: " + str(missing))

def read_thermo_qty(EOS_CompOSE, eosinfo, quantities_out, conv, error):
    """
    Reads the thermodynamic quantities from the CompOSE EOS and convert them 
    from natural units to cgs.
    """
    print("Reading thermodynamic quantities from EOS...")
    thermo_indices = EOS_CompOSE['Thermo_qty']['index_thermo'][...]
    epsilon, mu_q, mu_l = None, None, None
    for key in eosinfo:
        if eosinfo[key]["type"] != "thermodynamic":
            continue
        index = np.where(thermo_indices == int(eosinfo[key]["index"]))[0]
        
        if eosinfo[key]["title"] == "pressure p":
            pressure = np.squeeze((EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)
            if pressure.min() <= 0:
                warnings.warn("The pressure lower or equal than 0.")
                error = True
            with np.errstate(all='ignore'):
                quantities_out["logpress"] = np.log10(conv.pressure(pressure))
        
        if eosinfo[key]["title"] == "entropy per baryon S":
            quantities_out["entropy"] = np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)
        
        if eosinfo[key]["title"] == "shifted baryon chemical potential mu_b-m_n":
            quantities_out["mu_n"] = np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float) + \
                2 * conv.units.neutron_mass
        
        if eosinfo[key]["title"] == "charge chemical potential mu_q":
            mu_q = np.squeeze((EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)

        if eosinfo[key]["title"] == "lepton chemical potential mu_l":
            mu_l = np.squeeze((EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)
        
        if eosinfo[key]["title"] == "scaled internal energy per baryon E/m_n-1":
            energy = conv.specific_energy(np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float), 
                quantities_out["logrho"],
                EOS_CompOSE['Parameters']['nb'][...].astype(float))
            if energy.min() < 0:
                quantities_out["energy_shift"] = np.array(np.abs(energy.min()) * (1.001)).astype(float)
            elif energy.min() == 0:
                quantities_out["energy_shift"] = np.min(np.nonzero(energy)).astype(float)
            else:
                quantities_out["energy_shift"] = np.array(0).astype(float)
            quantities_out["logenergy"] = np.log10(energy + quantities_out["energy_shift"])
            quantities_out["dedt"] = Derive(10 ** quantities_out["logtemp"], energy, 1)
            del energy
        
        if eosinfo[key]["title"] == "square of speed of sound (c_s)^2 ":
            cs2 = np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)
            quantities_out["cs2"] = conv.speed_squared(cs2).astype(float)
        
        if eosinfo[key]["title"] == "epsilon (energy density)":
            epsilon = np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])).astype(float)

        if eosinfo[key]["title"] == "derivative dp/dn_b|E":
            quantities_out["dpdrhoe"] = conv.dpdrho(np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...]))).astype(float)
        
        if eosinfo[key]["title"] == "derivative p/dE|n_b":
            quantities_out["dpderho"] = conv.dpde(np.squeeze(
                (EOS_CompOSE['Thermo_qty']['thermo'][index, ...])), quantities_out["logrho"]).astype(float)
            
    check_mandatory_thermo_quantities(quantities_out, mu_q, mu_l, epsilon)

    ## Calculate chemical potentials
    quantities_out["mu_e"] = mu_l - mu_q
    quantities_out["mu_p"] = quantities_out["mu_n"] + mu_q
    quantities_out["muhat"] = quantities_out["mu_n"] - quantities_out["mu_p"]
    quantities_out["munu"] = quantities_out["mu_e"] - quantities_out["muhat"]

    ## Calculate gamma
    quantities_out["gamma"] = epsilon * cs2 / pressure

    ## Deallocate memory
    del pressure, cs2, epsilon, mu_q, mu_l
    print("Done.")
    return quantities_out, error
            
    
        
        