import numpy as np
from scipy.constants import physical_constants
from scipy.constants import h, c, e, N_A, electron_mass, epsilon_0
from matplotlib import pyplot as plt
esu_Cfactor=2997924579.9996


H_eV=physical_constants['Hartree energy in eV'][0]

def nm(wavelength, a=((h*c)/e)*10**9):
    return a/(wavelength)

def plot_tpaecd_nm(energie, rotatory, broadening=0.1, legend=None, linestyle=None):
    cross_sections = []
    k=1
    e1=0
    x=np.linspace(1,6,1000)
    plt.axhline(linewidth=1, color='black')
    for i in range(len(energie)):
        cross = k * ((x/H_eV))**2 * rotatory[i] * (broadening/H_eV) * ((2 * (x/H_eV) - (energie[i]/H_eV))**2 + (broadening/H_eV)**2 )**-1
        e1+=cross
        max_e1 = (max(cross))
        min_e1 = (min(cross))
        if abs(max_e1) > abs(min_e1):
            cross_sections.append(max_e1)
        else:
            cross_sections.append(min_e1)
    plt.plot(nm(x), e1, label=legend, linestyle=linestyle)
    # plt.bar([nm(i/2) for i in energie], cross_sections, width=2.5, color='r')
    return cross_sections

def plot_tpaecd_eV(energie, rotatory, broadening=0.1, legend=None, linestyle=None):
    cross_sections = []
    k=1
    e1=0
    x=np.linspace(1,6,1000)
    plt.axhline(linewidth=1, color='black')
    for i in range(len(energie)):
        cross = k * ((x/H_eV))**2 * rotatory[i] * (broadening/H_eV) * ((2 * (x/H_eV) - (energie[i]/H_eV))**2 + (broadening/H_eV)**2 )**-1
        e1+=cross
        max_e1 = (max(cross))
        min_e1 = (min(cross))
        if abs(max_e1) > abs(min_e1):
            cross_sections.append(max_e1)
        else:
            cross_sections.append(min_e1)
    plt.plot(x, e1, label=legend, linestyle=linestyle)
    plt.bar([i/2 for i in energie], cross_sections, width=0.025, color='r')
    return cross_sections