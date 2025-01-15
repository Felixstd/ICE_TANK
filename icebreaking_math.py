import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use('science')


#wave amplitude in mm. 
waveamp = np.arange(0, 10+0.5, 0.5)

fractures = np.zeros((2, 21))

#first experiment
fractures[0] = np.append(np.zeros(11), np.array([0.5, 1, 1, 1, 1,  1, 1, np.nan, np.nan, 4])) 

fractures[1] = np.append(np.zeros(16),np.array([ 0.5, np.nan, 1, np.nan, np.nan ]))
x = np.array([0.6, 2])
y = waveamp
X,Y = np.meshgrid(y,x)
print(np.shape(X), np.shape(fractures))
#second experiment 


fig = plt.figure(figsize = (4, 6))
ax = plt.axes()

pc = plt.pcolormesh(X, Y, fractures,shading='nearest', cmap = 'viridis', edgecolors = 'k')
ax.set_yticks(x)

ax.set_aspect('equal', adjustable = 'box')
# fig.colorbar(pc,ax = ax)
# cax = fig.add_axes([ax.get_position().x1+0.25,ax.get_position().y0,0.02,ax.get_position().y1-ax.get_position().y0])
# fig.colorbar(pc, ax=ax)
ax.set_xlabel('$A$ (mm)')
ax.set_ylabel(r'$h_i$ (cm)')
plt.savefig('frac.png')