import numpy as np
import os
import re
import sys
import scipy.constants as sc
from scipy.constants import h, c, e, N_A, epsilon_0
from scipy.constants import physical_constants
Bohrradius=physical_constants['Bohr radius'][0]
print(Bohrradius)

from operazioni import Sum_of_the_products, get_frequencies, number_of_states, read_file
from matrici import Matrix_P, Matrix_M, Matrix_T, Elec_trans_dip_moment, Magne_trans_dip_moment
from parse_file import parse_Dalton_file_2pa
b1,b2,b3=6,2,-2  #Two left circularly polarized (parallel)

##Equation 64, 65, 66, 67 J.Chem.Phys.125,064113 (2006)
def TpaRotatoryStr(file_in):
    stati=int(number_of_states(file_in))
    energies = parse_Dalton_file_2pa(file_in)[0]
    P=Matrix_P(file_in, stati)
    M=Matrix_M(file_in, stati)
    T=Matrix_T(file_in, stati)
    frequenze=get_frequencies(file_in, stati)
    RotatoryStr=[]
    B1_list=[]
    B2_list=[]
    B3_list=[]
    for i in range(0,stati,1):
        B1= -0.5 * frequenze[i]**-3 * Sum_of_the_products(M[i], P[i])
        B2=  0.5 * frequenze[i]**-3 * Sum_of_the_products(T[i], P[i])
        B3= -0.5 * frequenze[i]**-3 * np.trace(M[i])*np.trace(P[i])
        R=-b1*B1-b2*B2-b3*B3
        RotatoryStr.append(R)
        B1_list.append(B1)
        B2_list.append(B2)
        B3_list.append(B3)
    Dati = np.column_stack((energies, RotatoryStr, B1_list, B2_list, B3_list))
    np.savetxt("rot_B1_B2_B3", Dati, delimiter='  ', fmt='%0.4f')
    return RotatoryStr

def OpaRotatoryStr(file_in):
    Rot=[]
    stati=int(number_of_states(file_in))
    El_tr_dip = Elec_trans_dip_moment(file_in, stati)
    Mag_tr_dip = Magne_trans_dip_moment(file_in, stati)
    for i in range(0, stati, 1):
        rot = (3/4)*np.dot(El_tr_dip[i], Mag_tr_dip[i])
        Rot.append(rot)
    return Rot
