import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def plot_flexstrength(data_bup, data_samp, dic_dim_exp, dic_dim_samp, dir_files, dir_files_samp, Temp, Floe):
    
    lengths         = dic_dim_exp["lengths"]
    lb              = dic_dim_exp["lengths_fract"]
    width           = dic_dim_exp["width"]
    thickness       = dic_dim_exp['thickness']
    types_exp       = dic_dim_exp['type']
    x_loc           = dic_dim_exp['x']
    x_loc_before    = dic_dim_samp['x']
    y_loc           = dic_dim_exp['y']
    y_loc_before    = dic_dim_samp['y']
    if Temp:
        temperature = dic_dim_exp['Temp']
    if Floe:
        loc         = dic_dim_exp['loc']
        
    force_exp_samp, flex_strength_samp, unc_flex_strength_samp, vol_beams_samp, exp_samp, \
    time_samp = data_samp
    force_exp_bup, flex_strength_bup, unc_flex_strength_bup, vol_beams_bup, exp_bup, \
    time_bup = data_bup
         
    plt.figure(figsize = (5, 14))
    ax = plt.axes()
    ax.set_aspect('equal')
    plt.grid()
    plt.errorbar(exp_bup, flex_strength_bup/1e6, yerr = unc_flex_strength_bup/1e6, \
        marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
    plt.errorbar(exp_samp, flex_strength_samp/1e6, yerr = unc_flex_strength_samp/1e6, \
        marker = 'o', linestyle = '', color = 'blue', ecolor = 'black', capsize = 4)
    plt.xlabel('Experiments')
    plt.ylabel(r'$\sigma_c$ (MPa)')
    plt.savefig(dir_files+'/Flexural_strength.png')

    plt.figure(figsize = (5, 14))
    ax = plt.axes()
    ax.set_aspect('equal')
    plt.grid()
    plt.errorbar(exp_samp, flex_strength_samp/1e6, yerr = unc_flex_strength_samp/1e6, \
        marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
    plt.xlabel('Experiments')
    plt.ylabel(r'$\sigma_c$ (MPa)')
    plt.savefig(dir_files_samp+'/Flexural_strength.png')

    plt.figure()
    plt.hist(flex_strength_bup, bins=10, facecolor = None, edgecolor =  'black', fill = False)  # density=False would make counts
    plt.hist(flex_strength_samp, bins=5, facecolor = None, edgecolor =  'red', fill = False)
    plt.ylabel('Count')
    plt.xlabel(r'$\sigma_c$ (MPa)')
    plt.savefig(dir_files+'/Flexural_strength_hist.png')


    print(np.shape(x_loc), np.shape(flex_strength_bup))
    plt.figure(figsize = (5, 5))
    ax = plt.axes()
    ax.set_box_aspect(aspect=1)
    plt.grid()
    plt.scatter(x_loc, flex_strength_bup/1e6, c = y_loc, cmap = 'viridis')
    plt.scatter(x_loc_before, flex_strength_samp/1e6, marker = '*', c = y_loc_before, cmap = 'viridis')
    plt.xlabel(r'$x$ (cm)')
    plt.ylabel(r'$\sigma_c$ (MPa)')
    plt.savefig(dir_files+'/Flexural_strength_x.png')

    plt.figure(figsize = (5, 5))
    ax = plt.axes()
    ax.set_box_aspect(aspect=1)
    plt.errorbar(vol_beams_bup, flex_strength_bup/1e6, yerr = unc_flex_strength_bup/1e6, \
        marker = '*', linestyle = '', color = 'red', ecolor = 'black', capsize = 4)
    plt.grid()
    plt.legend()
    plt.xlabel(r'Volume (cm$^{3}$)')
    plt.ylabel('Flexural Strength (MPa)')
    plt.savefig(dir_files+'/Flexural_strength_volume.png')

    
    
    return 



def plot_time_load(data_samp, data_bup, dir_files, dir_files_samp):
    
    force_exp_samp, flex_strength_samp, unc_flex_strength_samp, vol_beams_samp, exp_samp, \
    time_samp = data_samp
    force_exp_bup, flex_strength_bup, unc_flex_strength_bup, vol_beams_bup, exp_bup, \
    time_bup = data_bup
    
    fig, axes = plt.subplots(nrows=7, ncols=6, figsize=(16, 14), constrained_layout=True)
    fig2, ax2 = plt.figure(), plt.axes()
    axes = np.array(axes).reshape(-1)
    i_idx, j_idx = np.meshgrid(np.arange(7), np.arange(6), indexing='ij')
    idx = np.vstack((i_idx.ravel(), j_idx.ravel())).T
    for exp, force_exp in enumerate(force_exp_bup) : 
        
        time_exp = time_bup[exp]
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
    
    
    # for expnum in range(0, len(force_exp_bup)):
        
    
    fig3, ax3 = plt.figure(figsize = (8, 4)), plt.axes()
    expnum = 12
    
    ind_max = np.argmax(force_exp_bup[expnum])
    ind_maxs = np.argsort(force_exp_bup[expnum])[::-1]
    diffs = np.diff(force_exp_bup[expnum])

    # Define a threshold for a "sharp decrease"
    threshold = -10  # Adjust this based on your data

    # Identify indices where the decrease is sharp
    sharp_decrease_indices = np.where(diffs < threshold)[0][0]

    
    time = time_bup[expnum]
    peaks, _ = find_peaks(force_exp_bup[expnum], distance=100)
    # ax3.set_box_aspect(aspect=1)
    ax3.plot(time, force_exp_bup[expnum], color = 'b')
    # ax3.scatter(time[0:sharp_decrease_indices], force_exp_bup[expnum][0:sharp_decrease_indices], marker = '*', color = 'black')
    # plt.xlim(4, 9)
    plt.ylabel('Force (N)', fontsize = 14)
    plt.xlabel('Time (s)', fontsize = 14)
    plt.savefig(dir_files+'force_load_{}_bup.png'.format(expnum))
    
    
    for expnum in range(0, len(force_exp_bup)):
        fig3, ax3 = plt.figure(figsize = (8, 4)), plt.axes()
        # expnum = 12
        # time = 
        # ind_max = np.argmax(force_exp_bup[expnum])
        # ind_maxs = np.argsort(force_exp_bup[expnum])[::-1]
        diffs_force = np.diff(force_exp_bup[expnum])
        diffs_time = np.diff(time_bup[expnum])

        # Define a threshold for a "sharp decrease"
        threshold_force = -10  # Adjust this based on your data
        threshold_time = 0.001
        
        print(np.shape(time_samp[expnum]), np.shape(force_exp_bup[expnum]))
        # Identify indices where the decrease is sharp
        sharp_decrease_indices = np.where((diffs_force < threshold_force) & (diffs_time>threshold_time))[0][0]
        print(sharp_decrease_indices)
        
        
        # peaks, _ = find_peaks(force_exp_samp[expnum], distance=100)
        # ax3.set_box_aspect(aspect=1)
        ax3.plot(time_bup[expnum], force_exp_bup[expnum], color = 'b')
        ax3.scatter(time_bup[expnum][sharp_decrease_indices], force_exp_bup[expnum][sharp_decrease_indices], marker = '*', color = 'black')
        # plt.xlim(4, 9)
        plt.ylabel('Force (N)', fontsize = 14)
        plt.xlabel('Time (s)', fontsize = 14)
        plt.savefig(dir_files+'force_load_{}_bup.png'.format(expnum))
    
    
    return 