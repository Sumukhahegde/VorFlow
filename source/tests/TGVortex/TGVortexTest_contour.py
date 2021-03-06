import numpy as np
import sys
sys.path.append('../../')
from mesh import *
from plotting import *
from solver import *
#N = 100
N = 40**2
L_x = 2.*np.pi
L_y = 2.*np.pi
dt = 0.001
Tend = 1.
nu = 0.1
rho = 1.0
#Re = 1.*L_x / nu
mesh = Mesh(N,L_x,L_y,np.zeros(4),'random')
#mesh = Mesh(N,L_x,L_y,np.ones(4),'cartesian')
data = Data(N);
for i in range(N):
		data.u_vel[i] = np.sin(mesh.centroid[i][0])*np.cos(mesh.centroid[i][1])
		data.v_vel[i] = -np.cos(mesh.centroid[i][0])*np.sin(mesh.centroid[i][1])
		#data.press[i] = np.exp(-((mesh.site[i,0]-L_x/2)**2 + (mesh.site[i,1]-L_y/2)**2))
		data.press[i] = (np.cos(mesh.centroid[i][0]*2.)+np.cos(mesh.centroid[i][1]*2.))/16.
u0 = data.u_vel
v0 = data.v_vel
P0 = data.press
x0 = np.zeros((N,1))
y0 = np.zeros((N,1))
for i in range(0, N):
        x0[i] = mesh.centroid[i][0]
        y0[i] = mesh.centroid[i][1]
t = 0.
#plt.ion()
data_old = data
while t < Tend:
                #for i in range(N):
                        #data.u_vel[i] = -np.sin(2.*np.pi/L_y * (mesh.centroid[i][1] - L_y/2.))
                        #data.v_vel[i] = np.sin(2.*np.pi/L_x * (mesh.centroid[i][0] - L_x/2.))
                        #data.u_vel[i] = -(mesh.centroid[i][1] - L_y/2.)/L_y
                        #data.v_vel[i] = (mesh.centroid[i][0] - L_x/2.)/L_x
                        #data.press[i] = mesh.area[i]/(2.*(L_x*L_y)/N)
#		Dx, Dy, L, Gx, Gy = time_step(mesh)
		data = time_step(mesh, data_old, dt, nu)
                mesh.update_mesh(data, dt)
                #plot_mesh(mesh);
                #make_frame(mesh,data.press,'Area')
                #plt.pause(0.005)
		data_old = data
                t += dt

# Function to plot solution with random points
from numpy import linspace, meshgrid
from matplotlib.mlab import griddata

def grid(xx, yy, zz, resX=100, resY=100):
	"Convert 3 column data to matplotlib grid"
	xi = np.linspace(min(xx), max(xx), resX)
	yi = np.linspace(min(yy), max(yy), resY)
	xx = xx[:,0]
	yy = yy[:,0]
	Z = griddata(xx, yy, zz, xi, yi, 'linear')
	X, Y = meshgrid(xi, yi)
	return X, Y, Z


# Plot solution
fig, ax = plt.subplots()
n = int(np.sqrt(N))
u_mat = np.reshape(data.u_vel, (n,n))
x = np.zeros((N,1))
y = np.zeros((N,1))
for i in range(0, N):
	x[i] = mesh.centroid[i][0]
	y[i] = mesh.centroid[i][1]
X = np.reshape(x,  (n,n))
Y = np.reshape(y,  (n,n))
X, Y, u_mat = grid(x, y, data.u_vel, n, n)
#print(X)
CS = plt.contourf(X, Y, u_mat, 20)
fig.colorbar(CS)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Numerical Sol')
plt.axis('scaled')
#plt.xlim([0.,mesh.L_x])
#plt.ylim([0.,mesh.L_y])
#plt.show(1)
# Plot initial
fig, ax = plt.subplots()
n = int(np.sqrt(N))
u_mat = np.reshape(u0, (n,n))
X = np.reshape(x0,  (n,n))
Y = np.reshape(y0,  (n,n))
X, Y, u_mat = grid(x, y, data.u_vel, n, n)
CS = plt.contourf(X, Y, u_mat, 20)
#cax = ax.imshow(u_mat, interpolation='nearest', cmap=cm.coolwarm)
fig.colorbar(CS)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Initial Condition')
plt.axis('scaled')
#plt.xlim([0.,mesh.L_x])
#plt.ylim([0.,mesh.L_y])
#plt.show()
# Numerical error
uA = np.zeros((N,1))
vA = np.zeros((N,1))
uError = np.zeros((N,1))
X = np.reshape(X, N)
Y = np.reshape(Y, N)
u_mat = np.reshape(u_mat, N)
for i in range(0, N):
	uA[i] = np.sin(X[i])*np.cos(Y[i])*np.exp(-2. *nu* Tend)
	#vA[i] = -np.cos(X[i])*np.sin(Y([i]))*np.exp(-2. *nu* Tend)
	uError[i] = abs(u_mat[i] - uA[i])
	#print(X[i])
	#if np.isnan(uA[i]):
		#print(X[i])
		#print(Y[i])
fig, ax = plt.subplots()
n = int(np.sqrt(N))
u_mat = np.reshape(uError, (n,n))
uError = uError[:,0]
X, Y, u_mat = grid(x, y, uError, n, n)
CS = plt.contourf(X, Y, u_mat, 20)
errorNorm = np.linalg.norm(uError, 2) / np.linalg.norm(uA, 2)
print(errorNorm)
#cax = ax.imshow(u_mat, interpolation='nearest', cmap=cm.coolwarm)
fig.colorbar(CS)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Error')
plt.axis('scaled')
fig, ax = plt.subplots()
n = int(np.sqrt(N))
u_mat = np.reshape(uA, (n,n))
X = np.reshape(x,  (n,n))
Y = np.reshape(y,  (n,n))
X, Y, u_mat = grid(x, y, data.u_vel, n, n)
CS = plt.contourf(X, Y, u_mat, 20)
#cax = ax.imshow(u_mat, interpolation='nearest', cmap=cm.coolwarm)
fig.colorbar(CS)
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.title('Analytical Solution')
plt.axis('scaled')
#print(mesh.centroid[1][0])
plt.show()

