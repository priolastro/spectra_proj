import numpy as np
import scipy.constants as sc
from scipy.constants import physical_constants
from scipy.constants import h, c, e, N_A, electron_mass, epsilon_0, electron_mass, hbar 
from matplotlib import pyplot as plt
esu_Cfactor = 2997924579.9996
Bohrradius=physical_constants['Bohr radius']
c0 = 137.03599858114194
eV = 0.03674932396442392
nanometer = 18.897261249935898
ElectricDipoleESU = 3.93430182850925E17
MagneticDipoleEMU = 5.391411336585763E19
centimeter = 1.8897261249935898E8 
second = 4.134137349487709E16
H_eV=physical_constants['Hartree energy in eV'][0]
# esuecd=e*Bohrradius*1E10*c*e*hbar/electron_mass*1E36 ##defined in dalton code

prefactors= {   ## Derived from https://doi.org/10.1021/jp1004659 (Computational Study of the One- and Two-Photon Absorption and Circular Dichroism of (l)-Tryptophan)
                ## gives opa and ecd in dm^3mol^-1cm^-1 and tpa and tpcd in 10^-50cm^4mol^-1photon^-1
                'None': 1,
                'opa' : 2*np.pi**2*N_A/(1000*np.log(10)*c0*centimeter**2),
                'ecd' : 64*np.pi**2*N_A/(9*1000*np.log(10)*c0**2*centimeter**2),
                'tpa' : (2*np.pi)**3*1E50/(30*c0**2*centimeter**4*second), ## se moltiplichi questo per 30 ottieni lo stesso valore di constant factor is defined after equation(10) in Phys. Chem. Chem. Phys., 2015,17, 19306-19314 (https://doi.org/10.1039/C5CP03241E)   k = (((8 * sc.pi ** 3 * sc.fine_structure * Bohrradius ** 5) / sc.speed_of_light) * 100000000) * 10 ** 50
                'tpcd' : 4*(2*np.pi)**3*1E50/(15*c0**3*centimeter**4*second),
            }

class Broadening_function():
    def __init__(self, tipo, broadening, x, energia):
        self.broadening = broadening
        self.tipo = tipo
        self.line = x
        self.energia = energia
    
    def __call__(self, tipo, broadening, x, energia):
        if tipo == 'gaussian':
            return (np.sqrt(2)) / (broadening / H_eV * np.sqrt(sc.pi)) * np.exp(-2 * ((x / H_eV) - (energia / H_eV))**2 / (broadening/ H_eV)**2)
        if tipo == 'lorentzian':
            return (1 / sc.pi) * (broadening / H_eV) * (((x / H_eV) - (energia / H_eV))**2 + (broadening / H_eV)**2)**-1

class Spectroscopy():
    def __init__(self, tipo):
        self.tipo = tipo

    def __call__(self, tipo, k, x):
        if tipo == 'opa':
            return k * x 
        if tipo == 'tpa':
            return k * x**2 





def nm(wavelength, a=((h*c)/e)*10**9):
    return a/(wavelength)


def plot_nm(energie, intensity, broadening, spectroscopy_type, lineshape , legend=None, linestyle=None, ax=plt):
    k=prefactors[spectroscopy_type]
    e1=0
    x=np.linspace(1,20,1000)
    function = Broadening_function(lineshape, broadening, x, energie)
    spectroscopy = Spectroscopy(spectroscopy_type)
    ax.axhline(linewidth=1, color='black')
    for i in range(len(energie)):
        e1 += spectroscopy(spectroscopy_type, k,x) * intensity[i] * function(lineshape, broadening, x, energie[i])
    ax.plot(nm(x), e1, label=legend, linestyle=linestyle)

# def plot_nm(energie, rotatory, broadening, function, spectroscopy, legend=None, linestyle=None, ax=plt):
#     k=prefactors[spectroscopy]
#     e1=0
#     x=np.linspace(1,20,1000)
#     ax.axhline(linewidth=1, color='black')
#     for i in range(len(energie)):
#         if function == 'Lorentzian':
#             if spectroscopy == 'ecd':
#                 e1 += k * x * rotatory[i] * Lorentzian(broadening, x, energie[i])
#             elif spectroscopy == 'tpcd':
#                 e1 += k * x**2 * rotatory[i] * Lorentzian(broadening, x, energie[i])
#         elif function == 'gaussian':
#             if spectroscopy == 'ecd':
#                 e1 += k * x * rotatory[i] * Gaussian(broadening, x, energie[i])
#             elif spectroscopy == 'tpcd':
#                 e1 += k * x**2 * rotatory[i] * Gaussian(broadening, x, energie[i])
#     ax.plot(nm(x), e1, label=legend, linestyle=linestyle)