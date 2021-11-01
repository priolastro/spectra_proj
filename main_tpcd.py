import argparse
from parse_file import parse_Dalton_file_2pa, parse_Dalton_file_1pa
from rotatory_strength import TpaRotatoryStr, OpaRotatoryStr
from plot_spectra import plot_tpaecd_nm, plot_tpaecd_eV
from matplotlib import pyplot as plt

parser = argparse.ArgumentParser(description = 'Plot tpcd-spectra')
parser.add_argument('file', type=str, help='Path of the input file with the TPCD calculation')
parser.add_argument('Spectroscopy', type=str, help='Type of spectroscopy', choices=['2PACD', '1PACD'])
parser.add_argument('xaxis', type=str, help='Set x axis scale', choices=['eV', 'nm'])
parser.add_argument('Broadening', type=float, help='Set broadening factor for Lorentzian lineshape (default set to 0.3)')
parser.add_argument('Interval', type=float, nargs='+', help='Set interval spectra in nm (default 100-500)')
parser.add_argument('-s', '--state', type=int, help='Set last number of state to plot')
parser.add_argument('-c', '--caption', type=str, help='Caption plot')
args = parser.parse_args()

plt.xlim(args.Interval)


if args.Spectroscopy == '2PACD':
    energies = None
    rotatory = None
    if args.state:
        energies = parse_Dalton_file_2pa(args.file)[0][:args.state]
        rotatory = TpaRotatoryStr(args.file)[:args.state]
    else:
        energies = parse_Dalton_file_2pa(args.file)[0]
        rotatory = TpaRotatoryStr(args.file)
    if args.xaxis == 'eV':
        cross_sections = plot_tpaecd_eV(energies, rotatory, broadening=args.Broadening, legend=args.caption)
    elif args.xaxis == 'nm':
        cross_sections = plot_tpaecd_nm(energies, rotatory, broadening=args.Broadening, legend=args.caption)
    
if args.Spectroscopy == '1PACD':
    energies = parse_Dalton_file_1pa(args.file)
    print(energies)
    opa_rotatory = OpaRotatoryStr(args.file)
    print(opa_rotatory)
    if args.xaxis == 'eV':
        plot_tpaecd_eV(energies, opa_rotatory, broadening=args.Broadening)
    elif args.xaxis == 'nm':
        plot_tpaecd_nm(energies, opa_rotatory, broadening=args.Broadening)
plt.legend()
plt.show()
