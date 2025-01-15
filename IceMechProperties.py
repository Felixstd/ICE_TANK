import numpy as np
import matplotlib.pyplot as plt
import scienceplots

"""
All of the stresses are in MPa. 
"""
plt.style.use('science')


def threepointbending():
    
    return


def cantilever():
    
    
    return

def Timco94(volume_brine):
    
    sigma_f = 1.76 * np.exp(-5.88 * np.sqrt(volume_brine))
    
    return sigma_f

def Dykins68(volume_brine):
    
    sigma_f = 1.044 - 2.275*np.sqrt(volume_brine)
    
    return sigma_f

def Truskov87(volume_brine):
    
    sigma_f = 0.8187*np.exp(-3.36*np.sqrt(volume_brine))
    
    return sigma_f
    
def Bogorodsky80(volume_brine):
    
    sigma_f = 0.7*(1-np.sqrt(volume_brine/0.202))
    
    return sigma_f

def krupina07(volume_brine):
    
    sigma_f = -0.346*np.sqrt(volume_brine) + 0.372
    
    return sigma_f

def karulina9(volume_brine, d):
    
    sigma_f = 0.5266*np.exp(-2.804 * np.sqrt(volume_brine))
    
    sigma_f_fresh = 0.9298*d**(0.2422)
    
    elastic = 4.299*np.exp(-2.071*d)
    
    return sigma_f, sigma_f_fresh, elastic

def williams94(volume_brine, volume, v_1 = 0.01):
    
    
    sigma_f = 1.76*(np.sqrt(volume_brine)*np.exp(-5.395))*(volume/v_1)**(-0.057)
    
    sigma_f_fresh = 1.629*(volume/v_1)**(-0.084)
    
    return sigma_f, sigma_f_fresh

def Aly19(volume, v_1 = 0.01):
    
    sigma_f_fresh = 0.840*(volume/v_1)**(-0.13)
    
    return sigma_f_fresh
    
v_brine = np.linspace(0, 0.25, 1000)
d = np.linspace(0, 1, 1000)


sigf_timco  = Timco94(v_brine)
sigf_dyk    = Dykins68(v_brine)
sigf_Trsusk = Truskov87(v_brine)
sigf_Bogor  = Bogorodsky80(v_brine)
sigf_krup   = krupina07(v_brine)
sigf_fresh_aly = Aly19(d**3)
sigf_will, sigf_fresh_will = williams94(v_brine, d**3)
sigf_karu, sigf_fresh_karu, elastic_fresh_karu = karulina9(v_brine, d)


fig, (ax1, ax2) = plt.subplots(1, 2, sharey = True, figsize = (7, 3))

axes = [ax1, ax2]
for ax in axes:
    ax.grid()
    # ax.set_aspect('equal', adjustable = 'box')
    ax.set_ylim(0, 2)

ax1.plot(np.sqrt(v_brine), sigf_dyk, color = 'b', label = 'Dykins, 1968')
ax1.plot(np.sqrt(v_brine), sigf_Bogor, color = 'g', label = 'Bogorodskiy et al., 1980')
ax1.plot(np.sqrt(v_brine), sigf_Trsusk, color = 'orange', label = 'Truskov et al., 1987')
ax1.plot(np.sqrt(v_brine), sigf_timco, color = 'r', label = 'Timco et al., 1994')
# ax1.plot(np.sqrt(v_brine), sigf_will, color = 'gray')
ax1.plot(np.sqrt(v_brine), sigf_krup, color = 'cyan', label  = 'Krupina et al., 2007')
ax1.plot(np.sqrt(v_brine), sigf_karu, color = 'k', label = 'Karulina et al., 2019')
ax1.set_xlabel(r'$\sqrt{\nu_b}$')
ax1.set_ylabel(r'$\sigma_f$ (MPa)')
ax1.text(-0.1, 1.1, '(a)', transform=ax1.transAxes, weight='bold')

ax2.plot(d**3, sigf_fresh_will, color = 'gray', label = 'Williams et al., 1994')
ax2.plot(d**3, sigf_fresh_karu, color = 'k')
ax2.plot(d**3, sigf_fresh_aly, color = 'saddlebrown', label = 'Aly et al., 2019')
ax2.set_xlabel(r'$d^3$ (m$^3$)')
ax1.text(-0.1, 1.1, '(b)', transform=ax2.transAxes, weight='bold')
# ax2.set_ylabel(r'$\sigma_f$ (MPa)')

fig.legend(loc = 'outside upper right', bbox_to_anchor = (1.2, 0.9))

plt.savefig('flex_strength.png')


