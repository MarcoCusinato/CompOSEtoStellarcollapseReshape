import os, json

def load_eosinfo(path):
    """
    The eos.info.json file contains the locations and names of all the variables
    in the eoscompose.h5
    """
    file_name = 'eos.info.json'
    path_to_file = os.path.join(path, file_name)
    print('Reading eos.info.json...')
    while not os.path.exists(path_to_file):
        print("\"" + file_name + "\" is missing in the given path.")
        file_name = input("Insert file name: ")
        path_to_file = os.path.join(path, file_name)
    with open(path_to_file, 'r') as f:
        parameters = json.load(f)['columns']
    if "-1" in parameters:
        parameters.pop("-1")
    return parameters