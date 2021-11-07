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
# parser.add_argument('xaxis', type=str, help='Set x axis scale', choices=['eV', 'nm'])
# parser.add_argument('Interval', type=float, nargs='+', help='Set interval spectra in nm (default 100-500)')
# parser.add_argument('-s', '--state', type=int, help='Set last number of state to plot')
# parser.add_argument('-c', '--caption', type=str, help='Caption plot')


args = parser.parse_args()


file_in = Output_file(args.file, args.Program, args.Spectroscopy)
print(file_in)
e = file_in.energies()
intensities = file_in.intensities()
plot_nm(e, intensities, args.Broadening, args.Spectroscopy, args.Lineshape)
plt.show()
