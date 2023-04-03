import h5py, os, numpy as np

def save_EOS(path, outputname, quantities_out):

    if not outputname.endswith('.h5'):
        outputname += '.h5'
    
    path_to_file = os.path.join(path, outputname)
    out_file = h5py.File(path_to_file, 'w')
    for key in quantities_out:
        if 'points' in key:
            out_file.create_dataset(key, shape = (1,), data = quantities_out[key])
        else:
            out_file.create_dataset(key, data = quantities_out[key])
    out_file.close()