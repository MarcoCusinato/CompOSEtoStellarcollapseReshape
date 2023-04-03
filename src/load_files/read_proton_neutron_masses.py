import os

def read_n_p_mass(path):
    """
    Some EOSs use different neutron and proton masses (from the usual ones).
    These valuse are stored in the first line of the eos.thermo
    """
    file_name = 'eos.thermo'
    path_to_file = os.path.join(path, file_name)
    print('Reading eos.thermo...')
    while (not os.path.exists(path_to_file)) and (file_name != 'None'):
        print("\"" + file_name + "\" is missing in the given path.")
        file_name = input("Insert file name (None if it does not exists): ")
        path_to_file = os.path.join(path, file_name)
    if file_name != 'None':
        with open(path_to_file, 'r') as f:
            masses = f.readlines()[0].split()
            masses = [float(m) for m in masses]
    else:
        print("Using standard neutron and proton masses (939.565420526 MeV and 938.27208816 MeV respectively).")
        masses = [939.565420526, 938.27208816]
    return masses[0], masses[1]