import numpy as np
import matplotlib.pyplot as plt
import scienceplots
import data 
import IceMechProperties as me
import plotting_mechproperties as plot

plt.style.use('science')

f1 = 10
f2 = 100
unc_dim = 0.3/100
unc_force = 0.1

data_sets = {
    "samples_1": {
        "files": data.data_files_04022025,
        "dim_file": data.file_dim_04022025,
        "dir": data.dir_04022025,
        "temp": data.Temperature_04022025,
        "floe": data.Floe_04022025,
    },
    "breakup_1": {
        "files": data.data_files_05022025,
        "dim_file": data.file_dim_05022025,
        "dir": data.dir_05022025,
        "temp": data.Temperature_05022025,
        "floe": data.Floe_05022025,
    },
    "samples_2":{
        "files": data.data_files_06022025,
        "dim_file": data.file_dim_06022025,
        "dir": data.dir_06022025,
        "temp": data.Temperature_06022025,
        "floe": data.Floe_06022025,
    },
    "breakup_2":{
        "files": data.data_files_07022025,
        "dim_file": data.file_dim_07022025,
        "dir": data.dir_07022025,
        "temp": data.Temperature_07022025,
        "floe": data.Floe_07022025,
    }
}

#------- Reading the data for all of the experiments ---------#

dim_data = {}
for key, d in data_sets.items():
    _, dim_data[key] = data.read_data(d["dir"], d["files"][0], d["dim_file"], 1, Floe = d["floe"], Temperature = d["temp"])


#------ Break up Experiment #1 -------#
data_bup1 = data.extract_data(data_sets["breakup_1"]['dir'],
                    data_sets["breakup_1"]['files'], 
                    data_sets["breakup_1"]['dim_file'], 
                    data_sets["breakup_1"]['floe'],
                    data_sets["breakup_1"]['temp'])
data_samp1 = data.extract_data(data_sets["samples_1"]['dir'],
                    data_sets["samples_1"]['files'], 
                    data_sets["samples_1"]['dim_file'], 
                    data_sets["samples_1"]['floe'],
                    data_sets["samples_1"]['temp'])
    
    
# #------ Break up Experiment #2 -------#
data_bup2 = data.extract_data(data_sets["breakup_2"]['dir'],
                    data_sets["breakup_2"]['files'], 
                    data_sets["breakup_2"]['dim_file'], 
                    data_sets["breakup_2"]['floe'],
                    data_sets["breakup_2"]['temp'])
data_samp2 = data.extract_data(data_sets["samples_2"]['dir'],
                    data_sets["samples_2"]['files'], 
                    data_sets["samples_2"]['dim_file'], 
                    data_sets["samples_2"]['floe'],
                    data_sets["samples_2"]['temp'])

plot.plot_flexstrength(data_bup1, 
                    data_samp1, 
                    dim_data['breakup_1'],
                    dim_data['samples_1'], 
                    data_sets["breakup_1"]['dir'], 
                    data_sets["samples_1"]['dir'], 
                    data_sets["breakup_1"]['temp'], 
                    data_sets["breakup_1"]['floe'])

plot.plot_time_load(data_samp1, 
                    data_bup1, 
                    data_sets["breakup_1"]['dir'], 
                    data_sets["samples_1"]['dir'])



force_exp_bup1, flex_strength_bup1, unc_flex_strength_bup1, vol_beams_bup1, exp_bup1, \
    time_bup1 = data_bup1
force_exp_bup2, flex_strength_bup2, unc_flex_strength_bup2, vol_beams_bup2, exp_bup2, \
time_bup2 = data_bup2

force_exp_samp1, flex_strength_samp1, unc_flex_strength_samp1, vol_beams_samp1, exp_samp1, \
    time_samp1 = data_samp1
force_exp_samp2, flex_strength_samp2, unc_flex_strength_samp2, vol_beams_samp2, exp_samp2, \
time_samp2 = data_samp2

flex_strength_tot = np.append(flex_strength_bup1, flex_strength_bup2)
flex_strength_samp = np.append(flex_strength_samp1, flex_strength_samp2)

mean_flex_strength = np.mean(flex_strength_tot)
mean_flex_samp = np.mean(flex_strength_samp)
std_flex = np.std(flex_strength_tot)
plt.figure()
plt.hist(flex_strength_tot/1e6, bins = 10, facecolor = None, edgecolor =  'black', fill = False)
plt.axvline(mean_flex_strength/1e6, color = 'r', label = 'mean')
plt.axvline(1.81, color = 'b', label = 'Parsons B. L. et al, 1992')
plt.axvline(2.1, color = 'g', label = 'Lavrov, V. V., 1971,')
plt.axvline(2.02, color = 'orange', label = 'Tatinclaux, J. C. et al 1978')
plt.ylabel('Count')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel(r'$\sigma_c$ (MPa)')
plt.savefig('Flexural_strength_hist_tot.png')
print(std_flex/1e6)


plt.figure()
plt.hist(flex_strength_tot/1e6, bins = 10, facecolor = None, edgecolor =  'black', fill = False)
plt.hist(flex_strength_samp/1e6, bins = 10, facecolor = None, edgecolor =  'blue', fill = False)
plt.axvline(mean_flex_strength/1e6, color = 'r', label = 'mean post')
plt.axvline(mean_flex_samp/1e6, color = 'g', label = 'mean pre')
plt.ylabel('Count')
# plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.legend()
plt.xlabel(r'$\sigma_c$ (MPa)')
plt.savefig('Flexural_strength_hist_comp_Samp.png')
# print(std_flex/1e6)
