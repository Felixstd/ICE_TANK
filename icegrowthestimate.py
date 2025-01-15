"""
This script is used to compute the ice thickness evolution 
to obtain an estimate of the time it would take to
form an ice sheet of thickness h_i. 
"""

import numpy as np
import matplotlib.pyplot as plt
import scienceplots

plt.style.use('science')


def icegrowth_OW(t, Ta, Tw, C, L, rho):

    dt = np.diff(t, prepend=t[0])
    print('dt', dt)
    growth_rates = np.maximum(0, C/(rho*L)*(Tw - Ta)*dt)

    thickness = np.cumsum(growth_rates[:len(t)])
        
    return thickness, growth_rates


def icegrowth_IB(t, T0, Tf, K, L, rho):
    
    dt = np.diff(t, prepend=t[0])
    growth = np.maximum(0, 2/(rho*L)*(K*(Tf-T0))*dt)
    
    thickness = np.sqrt(np.cumsum(growth[:len(t)]))
    growthrates = np.diff(thickness, prepend = thickness[0])/dt
    
    
    return thickness, growthrates

t =  np.arange(0, 4000+1, 1)*60
Ta, Tw =  -10, 0
Tf, T0 = 0, -10
C = 20
L = 3.34e5
rho = 1026
K = 2.03

time_exp1, temp_exp1 = np.loadtxt('time_temp_exp1_math.txt', skiprows = 1, unpack = True)
print(time_exp1)
time_exp1 = time_exp1*24*60*60
print(temp_exp1)

thickness_OW, growthrates_OW = icegrowth_OW(t, Ta, Tw, C, L, rho)
thickness_IB, growthrates_IB = icegrowth_IB(t, T0, Tf, K, L, rho)

thickness_OW_exp1, growthrates_OW_exp1 = icegrowth_OW(time_exp1, temp_exp1, Tw, C, L, rho)
thickness_IB_exp1, growthrates_IB_exp1 = icegrowth_IB(time_exp1, temp_exp1, Tf, K, L, rho)

print(thickness_IB_exp1)


fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (10, 5), sharey = True)

plt.legend()

axes = [ax1, ax2]

# for ax in axes:
#     ax.axis('equal')

ax1.plot(t/(60*60), growthrates_OW)
ax1.plot(t/(60*60), growthrates_IB)
ax1.set_xlabel(r'$t$ (hr)')
ax1.set_yscale('log')
ax1.set_ylabel(r'$dh/dt$ (m/s)')
ax1.grid()
ax1.text(-0.1, 1, '(a)', transform=ax1.transAxes, weight='bold')
# ax1.set_aspect('equal', adjustable='datalim')

ax2.text(-0.1, 1, '(b)', transform=ax2.transAxes, weight='bold')
ax2.plot(np.arange(0, len(thickness_OW_exp1)), growthrates_OW_exp1, label = 'OW')
ax2.plot(np.arange(0, len(thickness_IB_exp1)), growthrates_IB_exp1, label = 'IB')
ax2.set_yscale('log')
ax2.set_xlabel(r'$t$ (min)')
# ax2.set_aspect('equal', adjustable='datalim')
ax2.grid()

fig.legend(loc='upper center', bbox_to_anchor=(0.5, 0.00),
          fancybox=True, shadow=False, ncol=5)

plt.savefig('thickness_estimates.png')

