from src.load_files.load_compose_hdf5 import load_eosCompOSE
from src.load_files.load_eosinfo import load_eosinfo
from src.units_and_conversions.units import conversions
from src.read_qty.read_TrhoYe import read_TrhoYe
from src.read_qty.read_thermo_qty import read_thermo_qty
from src.read_qty.read_composition import read_mass_fractions
from src.read_qty.read_heavy_nuclei import read_heavy_nuclei
from src.save_files.save_EOS import save_EOS
from src.check_boundaries.check_boundaries import check_boundaries


def reshape_EOS(CompOSE_EOS_path, output_name):
    EOS_CompOSE = load_eosCompOSE(CompOSE_EOS_path)
    eosinfo = load_eosinfo(CompOSE_EOS_path)
    conv = conversions(CompOSE_EOS_path)
    quantities_out = {}
    error = False
    quantities_out = read_TrhoYe(EOS_CompOSE, eosinfo, quantities_out, conv)
    #print(quantities_out)
    quantities_out, error = read_thermo_qty(EOS_CompOSE, eosinfo, quantities_out, conv, error)
    quantities_out, error = read_mass_fractions(EOS_CompOSE, eosinfo, quantities_out, error)
    quantities_out, error = read_heavy_nuclei(EOS_CompOSE, eosinfo, quantities_out, error)
    check_boundaries(quantities_out, conv, error)
    EOS_CompOSE.close()
    save_EOS(CompOSE_EOS_path, output_name, quantities_out)
    pass

