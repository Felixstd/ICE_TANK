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

plotting = 0

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
    },
    "samples_3":{
    "files": data.data_files_12022025,
    "dim_file": data.file_dim_12022025,
    "dir": data.dir_12022025,
    "temp": data.Temperature_12022025,
    "floe": data.Floe_12022025,
    },
    "samples_4":{
    "files": data.data_files_13022025,
    "dim_file": data.file_dim_13022025,
    "dir": data.dir_13022025,
    "temp": data.Temperature_13022025,
    "floe": data.Floe_13022025,
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
    
    
#------ Break up Experiment #2 -------#
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

#------ Break up Experiment #3 -------#
data_samp3 = data.extract_data(data_sets["samples_3"]['dir'],
                    data_sets["samples_3"]['files'], 
                    data_sets["samples_3"]['dim_file'], 
                    data_sets["samples_3"]['floe'],
                    data_sets["samples_3"]['temp'])

#------ Break up Experiment #4 -------#
data_samp4 = data.extract_data(data_sets["samples_4"]['dir'],
                    data_sets["samples_4"]['files'], 
                    data_sets["samples_4"]['dim_file'], 
                    data_sets["samples_4"]['floe'],
                    data_sets["samples_4"]['temp'])

if plotting:
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


    plot.plot_time_load_experiment(data_samp1, data_sets["samples_1"]['dir'])
    plot.plot_time_load_experiment(data_samp2, data_sets["samples_2"]['dir'])
    plot.plot_time_load_experiment(data_samp3, data_sets["samples_3"]['dir'])
    plot.plot_time_load_experiment(data_samp4, data_sets["samples_4"]['dir'])
    plot.plot_time_load_experiment(data_bup1, data_sets["breakup_1"]['dir'])
    plot.plot_time_load_experiment(data_bup2, data_sets["breakup_2"]['dir'])


#----- Analysing all of the Statistics of the Tests Performed ------#

#---- Break-Up Data ----#
force_exp_bup1, flex_strength_bup1, unc_flex_strength_bup1, vol_beams_bup1, exp_bup1, \
    time_bup1, flexural_strength_buoyancy_bup1, sigmaf_3pt_bup1, sigmaf_cant_bup1, sigmaf_cantB_bup1 = data_bup1
force_exp_bup2, flex_strength_bup2, unc_flex_strength_bup2, vol_beams_bup2, exp_bup2, \
time_bup2, flexural_strength_buoyancy_bup2, sigmaf_3pt_bup2, sigmaf_cant_bup2, sigmaf_cantB_bup2 = data_bup2

#---- Samples Data ----#
force_exp_samp1, flex_strength_samp1, unc_flex_strength_samp1, vol_beams_samp1, exp_samp1, \
    time_samp1, flexural_strength_buoyancy_samp1, sigmaf_3pt_samp1, sigmaf_cant_samp1, sigmaf_cantB_samp1 = data_samp1
force_exp_samp2, flex_strength_samp2, unc_flex_strength_samp2, vol_beams_samp2, exp_samp2, \
time_samp2, flexural_strength_buoyancy_samp2, sigmaf_3pt_samp2, sigmaf_cant_samp2, sigmaf_cantB_samp2 = data_samp2
force_exp_samp3, flex_strength_samp3, unc_flex_strength_samp3, vol_beams_samp3, exp_samp3, \
time_samp3, flexural_strength_buoyancy_samp3, sigmaf_3pt_samp3, sigmaf_cant_samp3, sigmaf_cantB_samp3 = data_samp3
force_exp_samp4, flex_strength_samp4, unc_flex_strength_samp4, vol_beams_samp4, exp_samp4, \
time_samp4, flexural_strength_buoyancy_samp4, sigmaf_3pt_samp4, sigmaf_cant_samp4, sigmaf_cantB_samp4 = data_samp4



#----- Analysis of the flexural strength ------#

flex_strength_tot = np.append(flex_strength_bup1, flex_strength_bup2)
flex_strength_samp = np.append(flex_strength_samp1, np.append(flex_strength_samp2, np.append(flex_strength_samp3, flex_strength_samp4)))
flex_strength_samp_buoyancy = np.append(flexural_strength_buoyancy_samp1, np.append(flexural_strength_buoyancy_samp2, np.append(flexural_strength_buoyancy_samp3, flexural_strength_buoyancy_samp4)))
flex_strength_litt = data.LittData_FlexStrength_Laboratory['flexural']/1000 #Be in MPa


flex_strength_tot_3pt = np.append(sigmaf_3pt_bup1, np.append(sigmaf_3pt_bup2, \
    np.append(sigmaf_3pt_samp1, np.append(sigmaf_3pt_samp2, np.append(sigmaf_3pt_samp3, sigmaf_3pt_samp4)))))
flex_strength_tot_cant = np.append(sigmaf_cant_bup1, np.append(sigmaf_cant_bup2, \
    np.append(sigmaf_cant_samp1, np.append(sigmaf_cant_samp2, np.append(sigmaf_cant_samp3, sigmaf_cant_samp4)))))
flex_strength_tot_cant_B = np.append(sigmaf_cantB_bup1, np.append(sigmaf_cantB_bup2, \
    np.append(sigmaf_cantB_samp1, np.append(sigmaf_cantB_samp2, np.append(sigmaf_cantB_samp3, sigmaf_cantB_samp4)))))


mean_flex_litt = np.mean(flex_strength_litt)
mean_flex_strength = np.mean(flex_strength_tot)
mean_flex_samp = np.mean(flex_strength_samp)
mean_flex_buoyancy = np.mean(flex_strength_samp_buoyancy)
std_flex = np.std(flex_strength_tot)
std_litt = np.std(flex_strength_litt)

print(mean_flex_strength, mean_flex_samp, mean_flex_buoyancy, std_litt)

plt.figure()
ax = plt.axes()
plt.hist(flex_strength_tot/1e6, bins = 10, alpha = 0.5, facecolor = 'darkorange', edgecolor =  'None', fill = True)
plt.hist(flex_strength_samp/1e6, bins = 10, alpha = 0.5,facecolor = 'darkgreen', edgecolor =  'None', fill = True)
# plt.hist(flex_strength_samp_buoyancy/1e6, bins = 10, alpha = 0.5,facecolor = 'darkred', edgecolor =  'None', fill = True)
plt.axvline(mean_flex_strength/1e6, color = 'darkorange', linestyle = '--', label = 'Mean Post-Break-Up')
plt.axvline(mean_flex_litt, color = 'black', label = 'Mean Litt.')
plt.axvline(mean_flex_samp/1e6, linestyle = ':', color = 'green', label = 'Mean Pre-Break-Up')
plt.axvline(mean_flex_buoyancy/1e6, linestyle = '-', zorder = 1, linewidth = 2, color = 'darkred', label = 'Mean Buoyancy')
ax.axvspan(mean_flex_litt - std_litt, mean_flex_litt+ std_litt, alpha = 0.3, color = 'k')
plt.ylabel('Count')
plt.legend(loc='upper right')
plt.xlabel(r'$\sigma_c$ (MPa)')
plt.savefig('Flexural_strength_hist_tot.png')

plt.figure()
ax = plt.axes()
plt.hist(flex_strength_tot_3pt/1e6, bins = 10, alpha = 0.5, facecolor = 'darkorange', fill = False, hatch = '/')
plt.hist(flex_strength_tot_cant/1e6, bins = 5, alpha = 0.5,facecolor = 'darkgreen', fill = False, hatch = 'o')
plt.hist(flex_strength_tot_cant_B/1e6, bins = 5, alpha = 0.5,facecolor = 'darkred', fill = False, hatch = '*')
# plt.axvline(mean_flex_strength/1e6, color = 'darkorange', linestyle = '--', label = 'Mean Post-Break-Up')
# plt.axvline(mean_flex_litt, color = 'black', label = 'Mean Litt.')
# plt.axvline(mean_flex_samp/1e6, linestyle = ':', color = 'green', label = 'Mean Pre-Break-Up')
# plt.axvline(mean_flex_buoyancy/1e6, linestyle = '-', zorder = 1, linewidth = 2, color = 'darkred', label = 'Mean Buoyancy')
# ax.axvspan(mean_flex_litt - std_litt, mean_flex_litt+ std_litt, alpha = 0.3, color = 'k')
plt.ylabel('Count')
plt.legend(loc='upper right')
plt.xlabel(r'$\sigma_c$ (MPa)')
plt.savefig('Flexural_strength_tests_tot.png')



