import os, h5py

def load_eosCompOSE(path):
    """
    Load the CompOSE EOS file in hdf format from the given path.
    """
    file_name = 'eoscompose.h5'
    path_to_file = os.path.join(path, file_name)
    print('Reading eoscompose.h5...')
    while not os.path.exists(path_to_file):
        print("\"" + file_name + "\" is missing in the given path.")
        file_name = input("Insert file name: ")
        if not file_name.endswith('.h5'):
            file_name += '.h5'
        path_to_file = os.path.join(path, file_name)
    EOS_h5 = h5py.File(path_to_file)
    return EOS_h5