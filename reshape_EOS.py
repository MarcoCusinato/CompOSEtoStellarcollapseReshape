
from src.main import reshape_EOS

print('This script aims to reshape an EOS file generated with CompOSE to the stellarcollapse.org format.\n' + \
      'Please beware that this script is not perfect and may not work for all EOS files.\n' + \
      'So use it at your own risk.\n')

CompOSE_EOS_path = input('Enter the path to the CompOSE_EOS folder: ')
output_name = input('Enter the name of the output file: ')

reshape_EOS(CompOSE_EOS_path, output_name)
