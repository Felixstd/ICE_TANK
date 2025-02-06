import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import data 
import IceMechProperties as me

plt.style.use('science')


data_files = data.data_files_test
file_dim = data.file_dim_tests



flexural_strength = np.zeros(len(data_files))
unc_flexural_strength = np.zeros(len(data_files))
volume_beams = np.zeros(len(data_files))
experiments = np.arange(0, len(data_files))
f1 = 10
f2 = 100
unc_dim = 0.3/100
unc_force = 0.1

_, dic_dim = data.read_data(dir, data_files[0], file_dim, 1)
lengths = dic_dim["lengths"]
lb = dic_dim["lengths_fract"]
width = dic_dim["width"]
thickness = dic_dim['thickness']

#---- Analysing the forces -----#
fig, ((ax1, ax2, ax3, ax4), (ax5, ax6, ax7, ax8)) = plt.subplots(2, 4,
                         sharex=False, sharey=True, figsize = (12,6),layout='constrained')
axs = [ax1, ax2, ax3, ax4,ax5, ax6, ax7, ax8]

for exp, file in enumerate(data_files):
    ax = axs[exp]
    
    dic_exp, dic_dim = read_data(dir, file, file_dim, exp)
    
    force_exp = dic_exp['force']
    max_force = np.max(force_exp)
    length_exp, lb_exp, width_exp, thickness_exp = \
        lengths[exp]/100, lb[exp]/100, width[exp]/100, thickness[exp]/100
        
    volume_beams[exp] = length_exp*width_exp*thickness_exp*(100**3)
    
    flexural_strength[exp], unc_flexural_strength[exp] = \
        me.cantilever(max_force, lb_exp, width_exp, thickness_exp,unc_dim,unc_force, uncertainty=True )
        
    
    
    if exp < 3:
        time = dic_exp['timestep']*1/f1
    else:
        time = dic_exp['timestep']*1/f2
    
    # ax.set_aspect('equal', adjustable = 'datalim')
    ax.set_box_aspect(aspect=1)
    ax.plot(time, force_exp, color = 'b')
    
    ax.set_title('Exp. {}'.format(exp+1))
    fig.supylabel('Force (N)')
    fig.supxlabel('Time (s)')
    ax.grid()
    
plt.savefig('force.png'.format(exp))  

_, theory_flex = me.williams94(0, volume_beams/(100**3))


#---- plotting the flexural strength ----#

plt.figure(figsize = (6, 5))
ax = plt.axes()
ax.set_box_aspect(aspect=1)
plt.grid()
plt.errorbar(experiments, flexural_strength/1e6, yerr = unc_flexural_strength/1e6, \
    marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
plt.xlabel('Experiments')
plt.ylabel('Flexural Strength (MPa)')
plt.savefig('Flexural_strength.png')

plt.figure(figsize = (5, 5))
ax = plt.axes()
ax.set_box_aspect(aspect=1)
plt.errorbar(volume_beams, flexural_strength/1e6, yerr = unc_flexural_strength/1e6, \
    marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
plt.plot(volume_beams, theory_flex, color = 'blue', label = 'Williams et al. 1994')
plt.grid()
plt.legend()
plt.xlabel(r'Volume (cm$^{3}$)')
plt.ylabel('Flexural Strength (MPa)')
plt.savefig('Flexural_strength_volume.png')
    
