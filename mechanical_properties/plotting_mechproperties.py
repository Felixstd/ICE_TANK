import numpy as np
import matplotlib.pyplot as plt
import IceMechProperties as me
import matplotlib.lines as mlines

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
    time_samp, _ = data_samp
    force_exp_bup, flex_strength_bup, unc_flex_strength_bup, vol_beams_bup, exp_bup, \
    time_bup, _ = data_bup
         
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

def plot_flexural_strength_space(dim_data, data_flex):
    
    colors = ['steelblue', 'darkgreen', 'darkorange', 'darkred', 'darkviolet', 'gray']
    fig = plt.figure()
    ax = plt.axes()
    flexstrength = np.empty(0)
    flex_strength_door = np.empty(0)
    flex_strength_opposite = np.empty(0)
    # labels = ['Exp. 1']
    xlocations = np.empty(0)

    for i, dic in enumerate(dim_data):
        
        print(dic)
        
        # ax.text(0.1, 0.9, "({})".format(exp+1), size = 14, fontweight="heavy", transform=ax.transAxes)
        
        x_loc           = dim_data[dic]['x']
        xlocations = np.append(xlocations, x_loc)
        y_loc           = dim_data[dic]['y']
        data_exp = data_flex[i]
        
        _, flex_strength, unc_flexural_strength, _, _, \
        _, _, _, _, _ = data_exp
        c = 0
        for y in y_loc:
            if y < 50 : 
                
                plt.scatter(x_loc[c], flex_strength[c]/1e6,c = colors[i], marker = '*', zorder = 2)
                flex_strength_door = np.append(flex_strength_door, flex_strength[c])
            else:
                plt.scatter(x_loc[c], flex_strength[c]/1e6,c = colors[i], marker = '^', zorder = 2)
                flex_strength_opposite = np.append(flex_strength_opposite, flex_strength[c])
            c+=1
        flexstrength = np.append(flexstrength, flex_strength)
    
    
    mean = np.mean(flexstrength/1e6)
    std = np.std(flexstrength/1e6)
    corr = np.corrcoef(xlocations, flexstrength)
    print('Corr loc: ', corr)
    print('Mean everything: ', mean, std)
    mean_door = np.mean(flex_strength_door)/1e6
    mean_opp = np.mean(flex_strength_opposite)/1e6
    print(mean_door, mean_opp)
    
    # plt.axis('equal')
    plt.xlabel(r'$x$ (cm)')
    plt.ylabel(r'$\sigma_f$ (MPa)')
    plt.axhspan(mean-std, mean+std, alpha = 0.1, color = 'blue')
    # plt.axhline(mean_door, zorder = 1, color = 'k')
    # plt.axhline(mean, zorder = 1, color = 'orange')
    # plt.axhline(mean_opp, zorder = 1, color = 'r')
    door = mlines.Line2D([], [], color='k', marker='*', linestyle='None',
                          markersize=10, label='Door Side')
    ac = mlines.Line2D([], [], color='k', marker='^', linestyle='None',
                          markersize=10, label='A.C. Side')
    exp1 = mlines.Line2D([], [], color='steelblue', marker= 'None', linestyle='None',
                          markersize=10, label='4 Feb. 2025')
    exp2 = mlines.Line2D([], [], color='darkgreen', marker = 'None', linestyle='None',
                          markersize=10, label='5 Feb. 2025')
    exp3 = mlines.Line2D([], [], color='darkorange', marker='None', linestyle='None',
                          markersize=10, label='6 Feb. 2025')
    exp4 = mlines.Line2D([], [], color='darkred', marker='None', linestyle='None',
                          markersize=10, label='7 Feb. 2025')
    exp5 = mlines.Line2D([], [], color='darkviolet', marker='None', linestyle='None',
                          markersize=10, label='12 Feb. 2025')
    exp6 = mlines.Line2D([], [], color='gray', marker='None', linestyle='None',
                          markersize=10, label='13 Feb. 2025')
                          
    fig.legend(loc='center left', bbox_to_anchor=(0.85, 0.6), 
               handles=[door, ac, exp1, exp2, exp3, exp4, exp5, exp6], labelcolor='linecolor')
    plt.grid()
    plt.legend()
    plt.savefig('loc.png')
        
   
   
    
    
    return

def plot_time_load_experiment(data, dir_files):

    force_exps, _, _, _, _, time_exps, _, _, _, _ = data

    if len(force_exps) == 6:
        fig, axes = plt.subplots(nrows=2, ncols=3, sharex=True, figsize=(8, 4), constrained_layout=True)
        axes = np.array(axes).reshape(-1)
        i_idx, j_idx = np.meshgrid(np.arange(2), np.arange(3), indexing='ij')
    
    if len(force_exps) == 30:
        fig, axes = plt.subplots(nrows=5, ncols=6, sharex=True, figsize=(15, 12), constrained_layout=True)
        axes = np.array(axes).reshape(-1)
        i_idx, j_idx = np.meshgrid(np.arange(5), np.arange(6), indexing='ij')
    
    if len(force_exps) == 34:
        fig, axes = plt.subplots(nrows=7, ncols=6, sharex=True, figsize=(16, 14), constrained_layout=True)
        axes = np.array(axes).reshape(-1)
        i_idx, j_idx = np.meshgrid(np.arange(7), np.arange(6), indexing='ij')
    
    for exp, force_exp in enumerate(force_exps) : 
        
        time_exp = time_exps[exp]
        ax = axes[exp]
        ax.set_box_aspect(aspect=1)
        ax.plot(time_exp, force_exp, color = 'k')
    
        ax.text(0.1, 0.9, "({})".format(exp+1), size = 14, fontweight="heavy", transform=ax.transAxes)

        fig.supylabel('Force (N)', fontsize = 18)
        if len(force_exps) == 6:
            fig.supxlabel('Time (s)', y = -0.1, fontsize = 18)
        
        elif len(force_exps) == 34:
            fig.supxlabel('Time (s)', y = 0.11, fontsize = 18)
        else:
            fig.supxlabel('Time (s)', y = -0.05, fontsize = 18)
        ax.grid()

    plt.subplots_adjust(wspace=0.5, hspace=0.1) 
    
    if len(force_exps) == 34:
        for i in range(exp, len(axes)):
            axes[i].set_visible(False)
    
        
    plt.savefig(dir_files+'/force_time_load.png'.format(exp)) 
    
    
    

def plot_time_load(data_samp, data_bup, dir_files, dir_files_samp):
    
    force_exp_samp, flex_strength_samp, unc_flex_strength_samp, vol_beams_samp, exp_samp, \
    time_samp, _, _, _,_ = data_samp
    force_exp_bup, flex_strength_bup, unc_flex_strength_bup, vol_beams_bup, exp_bup, \
    time_bup, _, _, _ ,_= data_bup
    
    
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
        
    
    fig3, ax3 = plt.figure(figsize = (6, 5)), plt.axes()
    expnum = 12
    expnum_Samp = 4

    
    time = time_bup[expnum]
    force = force_exp_bup[expnum]
    time_Samp = time_samp[expnum_Samp]
    force_Samp = force_exp_samp[expnum_Samp]
    force_max, idx_max = me.maxforce_3point(force, time)
    
    time_samp = time_Samp-6

    time_samp[time_samp<0] = np.nan
    force_Samp[time_samp<0] = np.nan

    # cut =  np.shape(force_Samp)[0]-np.shape(force)[0]
    # plt.axis('equal')
    ax3.plot(time, force_exp_bup[expnum], color = 'k', label = 'Three Point Bending')
    # ax3.plot(time_Samp, force_Samp/max_force_bup, color = 'blue', label = 'Cantilever')
    ax3.axhline(force[idx_max], c = 'k', linestyle = '--', zorder = 3)
    # ax3.axhline(np.max(force_Samp)/max_force_bup, c = 'blue', linestyle = '--', zorder = 3)
    
    ax4 = ax3.twinx()
    # ax3.plot(time, force_exp_bup[expnum]/max_force_bup, color = 'k', label = 'Three Point Bending')
    ax4.plot(time_samp, force_Samp, color = 'blue', label = 'Cantilever')
    ax4.tick_params(axis='y', labelcolor='blue')
    # ax3.axhline(force[idx_max]/max_force_bup, c = 'k', linestyle = '--', zorder = 3)
    ax4.axhline(np.max(force_Samp), c = 'blue', linestyle = '--', zorder = 3)
    
    # plt.legend()
    plt.figtext(0.15, 0.8, 'Cantilever', color = 'blue', size = 14)
    plt.figtext(0.15, 0.72, 'Three Point Bending', color = 'black', size = 14)
    # ax3.set_aspect('equal')
    # ax4.set_aspect('equal')
    # plt.xlim(4, 9)
    ax3.set_ylabel('Force (N)', fontsize = 14)
    ax3.set_xlabel('Time (s)', fontsize = 14)
    plt.savefig(dir_files+'force_load_{}_bup.png'.format(expnum))
    
    
    
    return 