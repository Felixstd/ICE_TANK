import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import warnings

warnings.filterwarnings("ignore")


"""
All of the stresses are in MPa. 
"""
plt.style.use('science')

def maxforce_3point(force, time,threshold_force = -10, threshold_time = 0.001 ):
    
    diffs_force = np.diff(force)
    diffs_time = np.diff(time)

    # Identify indices where the decrease is sharp
    #Take the first one (subsequent ones are the one where the gauge hit the plate)
    idx_max_force = np.where((diffs_force < threshold_force) & (diffs_time>threshold_time))[0][0]

    max_force = force[idx_max_force
                      ]
    return max_force, idx_max_force

def threepointbending(F, l, b, hi, unc_dim, unc_f, uncertainty = False):
    """
    This function computes the flexural strength from cantiliver tests. 
    Args:
        F (_type_): Measured force at failure
        l (_type_): length of the ice samples
        b (_type_): width of the beam
        hi (_type_): ice thickness
    """
    
    sigma_f = (3/2)*F*l/(b*hi**2)
    if uncertainty:
        unc_F = (3/2)*l/(b*hi**2)*unc_f
        unc_l = (3/2)*F/(b*hi**2)*unc_dim
        unc_b = (3/2)*F*l/((b*hi)**2)*unc_dim
        unc_hi = 2*(3/2)*F*l/(b*hi**3)*unc_dim

        unc_sigmaf = np.sqrt(unc_F**2 + unc_l**2 + unc_b**2 + unc_hi**2)
    
        return sigma_f, unc_sigmaf
    
    
    
    else:
        return sigma_f
    
def cantilever(F, lb, b, hi, unc_dim, unc_f, uncertainty = False):
    """
    This function computes the flexural strength from cantiliver tests. 
    Args:
        F (_type_): Measured force at failure
        lb (_type_): length from the loading point to the location of crack
        b (_type_): width of the beam
        hi (_type_): ice thickness
    """
    sigma_f = 6*F*lb/(b*hi**2)
    if uncertainty:
        
        unc_F = 6*lb/(b*hi**2) * unc_f
        unc_lb = 6*F/(b*hi**2) * unc_dim
        unc_b  = 6*F*lb/(b**2*hi**2) * unc_dim
        unc_hi = 2*6*F*lb/(b*hi**3) * unc_dim
        
        unc_sigmaf = np.sqrt(unc_F**2 + unc_lb**2 + unc_b**2 + unc_hi**2)
        
        return sigma_f, unc_sigmaf
        
    else:
    
        return sigma_f

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

def deflection_air_cantilever(x, Force, L, b, h, E):
    
    I_moment = (b*h**3)/12
    
    y = Force*x**2*(3*L-x)/(6*E*I_moment)
    
    return y

def deflection_buoyancy_cantilever(x, Force, L, b, h, E, rhow = 1, g = 9.80):
    
    I_moment = (b*h**3)/12
    
    Lamda = (E*I_moment/(rhow*g*b))**(1/4)
    
    x_prime = x/(np.sqrt(2)*Lamda)
    x_prime_length = (L-x)/(np.sqrt(2)*Lamda)
    
    Length_caract = L/(np.sqrt(2)*Lamda)
    

    F = Force/(E*I_moment)
    
    y = np.sqrt(2)*F*Lamda**(3)/(E*I_moment)*(np.sinh(x_prime)*np.cos(x_prime_length)*np.cosh(Length_caract) - 
                                              np.sin(x_prime)*np.cosh(x_prime_length)*np.cos(Length_caract))/(
                                              np.cosh(Length_caract)**2 + np.cos(Length_caract)**2)
    return y

def sigmaf_buoyancyCanti(Force, L, b, h, E, rhow = 998, g = 9.80):
    
    I_moment = (b*h**3)/12
    
    Lamda = (E*I_moment/(rhow*g*b))**(1/4)
    
    
    Length_caract = L/(np.sqrt(2)*Lamda)

    F = Force
    
    sigmaf = (6*F*L/((b*h**2)))*(np.sqrt(2)*Lamda/L)*((np.cos(Length_caract)*np.sinh(Length_caract)+
                                                np.cosh(Length_caract)*np.sin(Length_caract))/
                                                (np.cosh(Length_caract)**2 + np.cos(Length_caract)**2))
    
    return sigmaf


  
v_brine = np.linspace(0, 0.25, 1000)
d = np.linspace(0, 1, 1000)
plotting = False
ElasticModulus = 3.2*1e9

exp_flex, sigma_f_exp, unc_sigmaf_exp = np.loadtxt('Theory/IceMechProp_Aly19.txt', skiprows = 1, unpack = True, dtype = str)

sigf_timco  = Timco94(v_brine)
sigf_dyk    = Dykins68(v_brine)
sigf_Trsusk = Truskov87(v_brine)
sigf_Bogor  = Bogorodsky80(v_brine)
sigf_krup   = krupina07(v_brine)
sigf_fresh_aly = Aly19(d**3)
sigf_will, sigf_fresh_will = williams94(v_brine, d**3)
sigf_karu, sigf_fresh_karu, elastic_fresh_karu = karulina9(v_brine, d)


if plotting:
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




