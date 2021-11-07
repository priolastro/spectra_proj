# from operazioni import number_of_states, read_file
import os, re, numpy as np
from matrici import Matrix_P, Matrix_M, Matrix_T, Elec_trans_dip_moment, Magne_trans_dip_moment
from operazioni import Sum_of_the_products, get_frequencies, number_of_states

class Output_file:

    def __init__(self, input_file, program, spectroscopy):
        assert isinstance(input_file, str)
        self.file_path = input_file
        self.name = os.path.split(input_file)[-1]
        self.program = program
        self.ROOTS = int(number_of_states(input_file, program))
        self.spectroscopy= spectroscopy

    def __str__(self):
        return f"{self.name} is {self.spectroscopy} {self.program} calculation with {self.ROOTS} root/s"

    def energies(self):
        energies = []
        with open(self.file_path, 'r') as file_object:
            out_output = file_object.readlines()
            for i, line in enumerate(out_output):
                if self.program == 'Dalton':
                    if 'Two-photon absorption summary' in line:
                        for l in range(i, i+5+(self.ROOTS*2)):
                            if 'Linear' in out_output[l]:
                                energy=float(out_output[l].split()[2])
                                energies.append(energy)
                    elif "@               Singlet electronic excitation energies" in line:
                        for cnt in range(0, self.ROOTS, 1): 
                            ener = float(out_output[i+7+cnt].split()[-1])
                            energies.append(ener)
                    elif "Singlet electronic excitation energies" in line:
                        for cnt in range(0, self.ROOTS, 1): 
                            ener = float(out_output[i+6+cnt].split()[-1])
                            energies.append(ener)
                if self.program == 'Gaussian':
                    if 'Excited State' in line:
                        row = line.split()
                        energies.append(float(row[4])) #extract energy in eV
        return energies

    def intensities(self):
        osc = []
        deltas = []
        sigmas = []
        Rot = []  ##for ecd dalton calculation
        if self.spectroscopy == 'opa' or self.spectroscopy == 'tpa':
            if self.program == 'Gaussian':
                with open(self.file_path, 'r') as file_object:
                    out_output = file_object.readlines()
                    for i, line in enumerate(out_output):
                        if 'Excited State' in line:
                            row = line.split()
                            osc.append(float(row[8].replace('f=',''))) 
                return osc
            elif self.program == 'Dalton':
                with open(self.file_path, 'r') as file_object:
                    out_output = file_object.readlines()
                    for i, line in enumerate(out_output):
                        if 'Two-photon absorption summary ' in line:
                            for l in range(i, i+5+(self.ROOTS*2)):
                                if 'Linear' in out_output[l]:
                                    D=float(out_output[l].split()[6])
                                    deltas.append(D)
                                    sigma=float(out_output[l].split()[7])
                                    sigmas.append(sigma)
                return deltas, sigmas
        elif self.spectroscopy == 'ecd' or self.spectroscopy == 'tpcd':
            if self.spectroscopy == 'ecd':           
                El_tr_dip = Elec_trans_dip_moment(self.file_path, self.ROOTS)
                Mag_tr_dip = Magne_trans_dip_moment(self.file_path, self.ROOTS)
                for i in range(0, self.ROOTS, 1):
                    rot = (3/4)*np.dot(El_tr_dip[i], Mag_tr_dip[i])
                    Rot.append(rot)
                return Rot
            elif self.spectroscopy == 'tpcd':
                ##Equation 64, 65, 66, 67 J.Chem.Phys.125,064113 (2006)
                b1,b2,b3=6,2,-2  #Two left circularly polarized (parallel)
                P=Matrix_P(self.file_path, self.ROOTS)
                M=Matrix_M(self.file_path, self.ROOTS)
                T=Matrix_T(self.file_path, self.ROOTS)
                frequenze=get_frequencies(self.file_path, self.ROOTS)
                RotatoryStr=[]
                B1_list=[]
                B2_list=[]
                B3_list=[]
                for i in range(0,self.ROOTS,1):
                    B1= -0.5 * frequenze[i]**-3 * Sum_of_the_products(M[i], P[i])
                    B2=  0.5 * frequenze[i]**-3 * Sum_of_the_products(T[i], P[i])
                    B3= -0.5 * frequenze[i]**-3 * np.trace(M[i])*np.trace(P[i])
                    R=-b1*B1-b2*B2-b3*B3
                    RotatoryStr.append(R)
                    B1_list.append(B1)
                    B2_list.append(B2)
                    B3_list.append(B3)
                # Dati = np.column_stack((energies, RotatoryStr, B1_list, B2_list, B3_list))
                # np.savetxt("rot_B1_B2_B3", Dati, delimiter='  ', fmt='%0.4f')
                return RotatoryStr   
