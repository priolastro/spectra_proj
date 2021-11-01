import re

def read_file(file):
    fin=open(file, 'r')
    lines=fin.readlines()
    return lines

def number_of_states(file, program):
    lines=read_file(file)
    if program == 'Dalton':
        for i, line in enumerate(lines):
            if "ROOT" in line or "NEXCIT" in line:
                root=lines[i+1]
                return root
            elif "Number of excitation energies:" in line:
                    root=float(line.split()[4])
                    return root
    if program == 'Gaussian':
        for i, line in enumerate(lines):
            if "NSTATES" in line:
                root = str(re.findall('NSTATES=([0-9]*)', line)[0])
                return root

def Sum_of_the_products(matrix1, matrix2):
    result=0
    for i in range(0,len(matrix1)):
        for j in range(0, len(matrix1)):
            result+=matrix1[i,j]*matrix2[i,j]
    return result

def get_frequencies(file, stati):
    frequenze=[]
    lines=read_file(file)
    for i, line in enumerate(lines):
        if "Two-photon transition tensor P (velocity gauge)" in line:
            for cnt in range(0, stati,1):
                freq=[i for i in lines[i+5+cnt].split()][2]
                frequenze.append(float(freq))
    return frequenze