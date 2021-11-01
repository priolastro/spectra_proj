import numpy as np
from operazioni import read_file, get_frequencies

def Elec_trans_dip_moment(file_in, stati):
    Etdms = []
    lines=read_file(file_in)
    for i, line in enumerate(lines):
        if "@               Electric transition dipole moments (au)" in line:
            for cnt in range(0, stati, 1): 
                eltrdip = [float(i) for i in lines[i+6+cnt].split()[-3:]]
                Etdms.append(eltrdip)
        elif "Electric transition dipole moments (in a.u.)" in line:
            for cnt in range(0, stati, 1): 
                eltrdip = [float(i) for i in lines[i+6+cnt].split()[-3:]]
                Etdms.append(eltrdip)
    return Etdms 

def Magne_trans_dip_moment(file_in, stati):
    Mtdms = []
    lines=read_file(file_in)
    for i, line in enumerate(lines):
        if "@               Magnetic transition dipole moments (au)" in line:
            for cnt in range(0, stati, 1): 
                magtrdip = [float(i) for i in lines[i+8+cnt].split()[-3:]]
                Mtdms.append(magtrdip)
        elif "Magnetic transition dipole moments (in a.u.)" in line:
            for cnt in range(0, stati, 1): 
                magtrdip = [float(i) for i in lines[i+8+cnt].split()[-3:]]
                Mtdms.append(magtrdip)
    return Mtdms

def Matrix_P(file_in, stati):
    Ps=[]
    lines=read_file(file_in)
    # frequenze=get_frequencies(file_in, stati)
    for i, line in enumerate(lines):
        if "Two-photon transition tensor P (velocity gauge)" in line:
            for cnt in range(0, stati, 1):
                P=np.zeros(shape=(3,3))
                tensor=[float(i) for i in lines[i+5+cnt].split()[3:]]
                P[0,0] = tensor[0]
                P[1,1] = tensor[1]
                P[2,2] = tensor[2]
                P[0,1]=P[1,0] =  tensor[3]
                P[0,2]=P[2,0] =  tensor[4]
                P[1,2]=P[2,1] =  tensor[5]
                Ps.append(P)
    return Ps

def Matrix_M(file_in, stati):
    Ms=[]
    lines=read_file(file_in)
    # frequenze=get_frequencies(file_in, stati)
    for i, line in enumerate(lines):
        if "El. dip.-mag. dip. trans. tensor  M (vel. gauge)" in line:
            for cnt in range(0, stati, 1):
                M=np.zeros(shape=(3,3))
                tensor=[float(i) for i in lines[i+5+cnt].split()[3:]]
                M[0,0] = tensor[0]
                M[1,1] = tensor[1]
                M[2,2] = tensor[2]
                M[0,1] = tensor[3]
                M[0,2] = tensor[4]
                M[1,0] = tensor[5]
                M[1,2] = tensor[6]
                M[2,0] = tensor[7]
                M[2,1] = tensor[8]
                Ms.append(M)
    return Ms

def Matrix_T(file_in, stati):
    T2ds=[]
    lines=read_file(file_in)
    # frequenze=get_frequencies(file_in, stati)
    for i, line in enumerate(lines):
        if "El. dip.-el. quad. trans. tensor  T (vel. gauge) " in line:
            for cnt in range(0, stati, 1): 
                    T2d=np.zeros(shape=(3,3))
                    T=np.zeros((3,3,3))
                    tensor=[float(i) for i in lines[i+5+cnt].split()[3:]]
                    for index, j in enumerate(tensor[0:3]):
                        T[index,0,0] = j                         
                    for index, j in enumerate(tensor[3:6]):
                        T[index,1,1] = j
                    for index, j in enumerate(tensor[6:9]):
                        T[index,2,2] = j
                    for index, j in enumerate(tensor[9:12]):
                        T[index,0,1] = T[index,1,0] = j
                    for index, j in enumerate(tensor[12:15]):
                        T[index,0,2] = T[index,2,0] = j
                    for index, j in enumerate(tensor[15:18]):
                        T[index,1,2] = T[index,2,1] = j
                    ##diagonal elements xx,yy,zz
                    T2d[0,0] =  (T[2,1,0] - T[1,2,0]) 
                    T2d[1,1] =  (T[0,2,1] - T[2,0,1]) 
                    T2d[2,2] =  (T[1,0,2] - T[0,1,2]) 
                    ##off diagonal elements xy,xz,yx,zx,yz,zy
                    T2d[0,1] =  T[0,2,0] - T[2,0,0]
                    T2d[0,2] =  T[1,0,0] - T[0,1,0]
                    T2d[1,0] = T[2,1,1] - T[1,2,1]
                    T2d[2,0] = T[2,1,2] - T[1,2,2]
                    T2d[1,2] = T[1,0,1] - T[0,1,1]
                    T2d[2,1] = T[0,2,2] - T[2,0,2]
                    T2ds.append(T2d)
    return T2ds
