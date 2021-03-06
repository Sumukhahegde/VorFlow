import numpy as np
import sys
sys.path.append('../../../')
from mesh import *
from plotting import *
from solver import *
import pickle

# AW --
Nx = 150
N = Nx**2
L_x = 2.*np.pi
L_y = 2.*np.pi
dt = 1./Nx
dTPlot = 0.01
Tend = 3.
nu = 0.01
rho = 1.

mesh = Mesh(N,L_x,L_y,np.zeros(4),'random')
data = Data(N);

for i in range(N):
	data.u_vel[i] = np.sin(mesh.centroid[i][0])*np.cos(mesh.centroid[i][1])
	data.v_vel[i] = -np.cos(mesh.centroid[i][0])*np.sin(mesh.centroid[i][1])

t = 0.
tprint = 0.
data = time_step(mesh,data,0,nu)  # Initial projection...
#ax = plt.gca()
i = 0;
while t < Tend:
	if t >= tprint:
		tprint += dTPlot;
		#u_exact = np.zeros(N);
		#for j in range(N):
			#u_exact[j] = np.sin(mesh.centroid[j][0])*np.cos(mesh.centroid[j][1])* np.exp(-2.*nu*t)
		u_exact = np.zeros(N);
                errorVec = np.zeros(N)
                for j in range(N):
                	u_exact[j] = np.sin(mesh.centroid[j][0])*np.cos(mesh.centroid[j][1])* np.exp(-2.*nu*t)
                	errorVec[j] = abs(data.u_vel[j] - u_exact[j]) / abs(u_exact[j])
		#save_frame(mesh,0.5*(data.u_vel**2+data.v_vel**2),'Energy',t,ax,'output/energy'+'{:04d}'.format(i)+'.png',False)
		#save_frame(mesh,data.press,'Pressure',t,ax,'output/pressure'+'{:04d}'.format(i)+'.png',False)
		#save_frame(mesh,np.abs(data.u_vel-u_exact),'Error',t,ax,'output/error'+'{:04d}'.format(i)+'.png',False)
		filename = './outputLocal/output'+'{:04d}'.format(i)+'.p';
		fileObject = open(filename,'wb')
		pickle.dump([mesh,data,t,u_exact, errorVec],fileObject);
		fileObject.close()
		i += 1;
	
	data = time_step(mesh,data,dt,nu)
        mesh.update_mesh(data, dt)
        t+= dt
	print(t)
