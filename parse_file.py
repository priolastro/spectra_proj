from operazioni import number_of_states, read_file
import os

class Output_file:

    def __init__(self, input_file, program, spectroscopy):
        assert isinstance(input_file, str)
        self.file_path = input_file
        self.name = os.path.split(input_file)[-1]
        self.program = program
        self.ROOTS = int(number_of_states(self.file_path, self.program))
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
                if self.program == 'Gaussian':
                    if 'Excited State' in line:
                        row = line.split()
                        energies.append(float(row[4])) #extract energy in eV
        return energies

    def oscillator(self):
        osc = []
        with open(self.file_path, 'r') as file_object:
            out_output = file_object.readlines()
            for i, line in enumerate(out_output):
                if self.program == 'Gaussian':
                    if 'Excited State' in line:
                        row = line.split()
                        osc.append(float(row[8].replace('f=',''))) 
        return osc


    def deltas(self):
        deltas = []
        with open(self.file_path, 'r') as file_object:
            out_output = file_object.readlines()
            for i, line in enumerate(out_output):
                if 'Two-photon absorption summary ' in line:
                    for l in range(i, i+5+(self.ROOTS*2)):
                        if 'Linear' in out_output[l]:
                            D=float(out_output[l].split()[6])
                            deltas.append(D)
        return deltas

    def sigma(self):
        sigmas = []
        with open(self.file_path, 'r') as file_object:
            out_output = file_object.readlines()
            for i, line in enumerate(out_output):
                if 'Two-photon absorption summary ' in line:
                    for l in range(i, i+5+(self.ROOTS*2)):
                        if 'Linear' in out_output[l]:
                            sigma=float(out_output[l].split()[7])
                            sigmas.append(sigma)
        return sigmas    
