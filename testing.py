nop =[0,1,2,3,4,5,6,11,12,17,18,23,24,29,30,31,32,33,34,35]
import numpy as np
def recursive_look_direction(pos, dir, m,color):
    # return -1 si no puede en esa direcion
    if(m[pos+dir]==0):
        print('se puede jugar en la posicion: ',pos+dir)
        return pos+dir
    if(m[pos+dir]==color):
        #se revisa en la sig
        return -1
    else: # entonces es el color contrario
        if pos+dir in nop:
            return -1
        else:
            print('arriba tengo un enemigo')
            return recursive_look_direction(pos+dir,dir, m,color)

def possible_moves(l,pos,dir,color):
    #list_pm =[]
    if pos+dir <0 and pos+dir >=36:
        return -1
    if (l[pos+dir]==-1*color):
        p=recursive_look_direction(pos+dir,dir,l,color)
        if p!=-1:
            return p
    else: #posicions hay 0 
        return -1
        

m= [0 for i in range(6**2)]
m[14]=1
m[21]=1
m[15]=-1

m[20]=-1
#m[9]=1
#m[3]=-1
print(m)
list_pm=[]
moves=[1,-1,-6,6,5,-5,7,-7]
#print(list(np.where(np.array(m) == 1)[0]))
for i in list(np.where(np.array(m) == 1)[0]):
    for j in moves:
        pm=possible_moves(m,i,j,-1)
        if pm !=-1:
            list_pm.append(pm)
print(list_pm)