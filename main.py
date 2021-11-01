import argparse
import sys
from matplotlib import pyplot as plt

from parse_file import Output_file
from plot_functions import plot_nm


print("""                                                                                                  
      _/_/_/                                  _/                                                  
   _/        _/_/_/      _/_/      _/_/_/  _/_/_/_/  _/  _/_/    _/_/_/      _/_/_/    _/    _/   
    _/_/    _/    _/  _/_/_/_/  _/          _/      _/_/      _/    _/      _/    _/  _/    _/    
       _/  _/    _/  _/        _/          _/      _/        _/    _/      _/    _/  _/    _/     
_/_/_/    _/_/_/      _/_/_/    _/_/_/      _/_/  _/          _/_/_/  _/  _/_/_/      _/_/_/      
         _/                                                              _/              _/       
        _/                                                              _/          _/_/          
        by Salvatore Prioli""")

parser = argparse.ArgumentParser(description = 'Plot spectra')
parser.add_argument('file', type=str, help='file input path')
parser.add_argument('Program', type=str, help='file input program', choices=['Dalton', 'Gaussian'])
parser.add_argument('Spectroscopy', type=str, help='Type of spectroscopy', choices=['opa', 'tpa', 'ecd', 'tpcd'])
parser.add_argument('Lineshape', type=str, help='gaussian or lorentzian', choices=['gaussian', 'lorentzian'])
parser.add_argument('Broadening', type=float, help='Set broadening factor')
args = parser.parse_args()


file_in = Output_file(args.file, args.Program, args.Spectroscopy)
e = file_in.energies()
osc = file_in.oscillator()
plot_nm(e, osc, args.Broadening, args.Spectroscopy, args.Lineshape)
plt.show()
