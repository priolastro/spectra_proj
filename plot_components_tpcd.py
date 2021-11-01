import numpy as np
import sys 
import matplotlib.pyplot as plt
from scipy.constants import h, c, e

def nm(wavelength, a=((h*c)/e)*10**9):
    return a/(wavelength)

file_in631G = sys.argv[1]
file_incc = sys.argv[2]

ener_631G, rot_631G, B1_631G, B2_631G, B3_631G = np.loadtxt(file_in631G, unpack=True)
ener_cc, rot_cc, B1_cc, B2_cc, B3_cc = np.loadtxt(file_incc, unpack=True)


fig,(ax1,ax2,ax3) = plt.subplots(3,1)
ax1.bar([nm(i)*2 for i in ener_631G], [i for i in B1_631G], width=1, label='6-31+G*')
ax1.bar([nm(i)*2 for i in ener_cc], [i for i in B1_cc], width=1, label='aug-cc-pVDZ')
ax2.bar([nm(i)*2 for i in ener_631G], B2_631G, width=1, label='6-31+G*')
ax2.bar([nm(i)*2 for i in ener_cc], B2_cc, width=1, label='aug-cc-pVDZ')
ax3.bar([nm(i)*2 for i in ener_631G], B3_631G, width=1, label='6-31+G*')
ax3.bar([nm(i)*2 for i in ener_cc], B3_cc, width=1, label='aug-cc-pVDZ')
ax1.legend()
ax2.legend()
ax3.legend()
ax2.set_xlabel('Wavelenght (nm)')
ax1.set_ylabel('$B_1$')
ax2.set_ylabel('$B_2$')
ax3.set_ylabel('$B_3$')
ax1.axhline(y=0, color='black',linewidth=1)
plt.tight_layout()
plt.show()

# fig,(ax4) = plt.subplot(1,1)
plt.bar([nm(i)*2 for i in ener_631G], rot_631G, width=1, label='6-31+G*')
plt.bar([nm(i)*2 for i in ener_cc], rot_cc, width=1, label='aug-cc-pVDZ')
plt.show()