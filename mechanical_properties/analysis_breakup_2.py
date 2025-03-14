import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import data 
import IceMechProperties as me

plt.style.use('science')

f1 = 10
f2 = 100
unc_dim = 0.3/100
unc_force = 0.1

#---- Second Break-up Experiment -----#
#--- After Before Break-up Experiment ---#
data_files_bef = data.data_files_06022025
file_dim_bef = data.file_dim_06022025
dir_files_bef = data.dir_06022025
Temp_bef = data.Temperature_06022025
Floe_bef = data.Floe_06022025

#--- After Break-up Experiment ---#
data_files = data.data_files_07022025
file_dim = data.file_dim_07022025
dir_files = data.dir_07022025
Temp = data.Temperature_07022025
Floe = data.Floe_07022025


flexural_strength = np.zeros(len(data_files))
unc_flexural_strength = np.zeros(len(data_files))
volume_beams = np.zeros(len(data_files))
experiments = np.arange(0, len(data_files))


_, dic_dim = data.read_data(dir_files, data_files[0], file_dim, 1, Floe = data.Floe_07022025, Temperature=Temp )
_, dic_dim_bef = data.read_data(dir_files_bef, data_files_bef[0], file_dim_bef, 1, Floe_bef, Temperature=Temp_bef )

lengths = dic_dim["lengths"]
lb = dic_dim["lengths_fract"]
width = dic_dim["width"]
thickness = dic_dim['thickness']
types_exp = dic_dim['type']
x_loc = dic_dim['x']
x_loc_before = dic_dim_bef['x']
y_loc = dic_dim['y']
if Temp:
    temperature = dic_dim['Temp']
if Floe:
    loc = dic_dim['loc']


force_experiments, flexural_strength, unc_flexural_strength, volume_beams, experiments, time = \
    data.extract_data(dir_files, data_files, file_dim, Floe, Temp)
force_experiments_before, flexural_strength_before, unc_flexural_strength_before, volume_beams_before, experiments_before, time_before = \
    data.extract_data(dir_files_bef, data_files_bef, file_dim_bef, Floe_bef, Temp_bef)

fig, axes = plt.subplots(nrows=7, ncols=6, figsize=(16, 14), constrained_layout=True)
fig2, ax2 = plt.figure(), plt.axes()
axes = np.array(axes).reshape(-1)
i_idx, j_idx = np.meshgrid(np.arange(7), np.arange(6), indexing='ij')
idx = np.vstack((i_idx.ravel(), j_idx.ravel())).T
for exp, force_exp in enumerate(force_experiments) : 
    
    time_exp = time[exp]
    ax = axes[exp]
    ax.set_box_aspect(aspect=1)
    ax.plot(time_exp, force_exp, color = 'b')
    
    ax2.plot(time_exp, force_exp)

    fig.supylabel('Force (N)', fontsize = 18)
    fig.supxlabel('Time (s)', y = 0.11, fontsize = 18)
    ax.grid()

plt.subplots_adjust(wspace=0.1, hspace=0.4) 
for i in range(exp, len(axes)):
    axes[i].set_visible(False)
    
plt.savefig(dir_files+'/force_2.png'.format(exp))  
ax2.set_box_aspect(aspect=1)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Force (N)')
plt.savefig(dir_files+'/force_tot.png'.format(exp))  



# _, theory_flex = me.williams94(0, volume_beams/(100**3))


# #---- plotting the flexural strength ----#

plt.figure(figsize = (5, 14))
ax = plt.axes()
ax.set_aspect('equal')
plt.grid()
plt.errorbar(experiments, flexural_strength/1e6, yerr = unc_flexural_strength/1e6, \
    marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
plt.errorbar(experiments_before, flexural_strength_before/1e6, yerr = unc_flexural_strength_before/1e6, \
    marker = 'o', linestyle = '', color = 'blue', ecolor = 'black', capsize = 4)
plt.xlabel('Experiments')
plt.ylabel(r'$\sigma_c$ (MPa)')
plt.savefig(dir_files+'/Flexural_strength.png')

plt.figure(figsize = (5, 14))
ax = plt.axes()
ax.set_aspect('equal')
plt.grid()
plt.errorbar(experiments_before, flexural_strength_before/1e6, yerr = unc_flexural_strength_before/1e6, \
    marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
plt.xlabel('Experiments')
plt.ylabel(r'$\sigma_c$ (MPa)')
plt.savefig(dir_files_bef+'/Flexural_strength.png')

plt.figure()
plt.hist(flexural_strength, bins=15, facecolor = None, edgecolor =  'black', fill = False)  # density=False would make counts
plt.hist(flexural_strength_before, bins=5, facecolor = None, edgecolor =  'red', fill = False)
plt.ylabel('Count')
plt.xlabel(r'$\sigma_c$ (MPa)')
plt.savefig(dir_files+'/Flexural_strength_hist.png')

# plt.figure(figsize = (5, 5))
# ax = plt.axes()
# ax.set_box_aspect(aspect=1)
# plt.grid()
# plt.scatter(temperature, flexural_strength/1e6, color = 'red')
# plt.xlabel(r'$T_s$ (°C)')
# plt.ylabel(r'$\sigma_c$ (MPa)')
# plt.savefig(dir_files+'/Flexural_strength_Temp.png')

plt.figure(figsize = (5, 5))
ax = plt.axes()
ax.set_box_aspect(aspect=1)
plt.grid()
plt.scatter(x_loc, flexural_strength/1e6, color = 'red')
plt.scatter(x_loc_before, flexural_strength_before/1e6, color = 'blue')
plt.xlabel(r'$x$ (cm)')
plt.ylabel(r'$\sigma_c$ (MPa)')
plt.savefig(dir_files+'/Flexural_strength_x.png')

# plt.figure(figsize = (5, 5))
# ax = plt.axes()
# ax.set_box_aspect(aspect=1)
# plt.errorbar(volume_beams, flexural_strength/1e6, yerr = unc_flexural_strength/1e6, \
#     marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
# plt.plot(volume_beams, theory_flex, color = 'blue', label = 'Williams et al. 1994')
# plt.grid()
# plt.legend()
# plt.xlabel(r'Volume (cm$^{3}$)')
# plt.ylabel('Flexural Strength (MPa)')
# plt.savefig(dir_files+'/Flexural_strength_volume.png')


    
