import numpy as np
import warnings

def check_boundaries(quantities_out, conv, error):
    """
    Checks if the values of the quantities are within the boundaries of the EOS.
    """
    if (quantities_out["cs2"] > conv.units.c ** 2).any():
        warnings.warn("The sound speed squared is larger than the speed of light.")
        error = True
    if (quantities_out["gamma"] < 1.0).any():
        warnings.warn("The adiabatic index is smaller than 1.")
        error = True
    if error:
        warnings.warn("Some quantities have unphysical values. To fix this, try to run CompOSE with a lower number of grid points.")
    
    