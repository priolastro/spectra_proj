from operazioni import number_of_states, read_file

def parse_Dalton_file_2pa(file):
    ROOTS= None
    energies = []
    deltas = []
    sigmas = []
    with open(file, 'r') as file_object:
        out_output = file_object.readlines()
        for i, line in enumerate(out_output):
            if ".ROOTS" in line:
                ROOTS=int(out_output[i+1])
            elif 'Two-photon absorption summary ' in line:
                for l in range(i, i+5+(ROOTS*2)):
                    if 'Linear' in out_output[l]:
                        energy=float(out_output[l].split()[2])
                        D=float(out_output[l].split()[6])
                        sigma=float(out_output[l].split()[7])
                        energies.append(energy)
                        deltas.append(D)
                        sigmas.append(sigma)
    return energies, deltas, sigmas

def parse_Dalton_file_1pa(file):
    stati=int(number_of_states(file))
    energies = []
    lines=read_file(file)
    for i, line in enumerate(lines):
        if "@               Singlet electronic excitation energies" in line:
            for cnt in range(0, stati, 1): 
                ener = float(lines[i+7+cnt].split()[-1])
                energies.append(ener)
        elif "Singlet electronic excitation energies" in line:
            for cnt in range(0, stati, 1): 
                ener = float(lines[i+6+cnt].split()[-1])
                energies.append(ener)
    return energies 
