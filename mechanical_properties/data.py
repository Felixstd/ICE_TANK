import numpy as np
import os
import IceMechProperties as me

def read_data(dir, filename_force, filename_dim, exp, Tests = False, Floe = False, Temperature = False):
    """
    This is a function used to read the data from the force gauge. 

    Args:
        dir (_type_): _description_
        filename_force (_type_): _description_
        filename_dim (_type_): _description_
        exp (_type_): _description_

    Returns:
        _type_: _description_
    """
    
    #--- This part is only for the preliminary results ---#
    
    data_dim = np.loadtxt(os.path.join(dir, filename_dim), skiprows=1, delimiter=',', dtype=str)

    skip_header = 7 if (Tests and exp < 3) else 2
    data = np.genfromtxt(os.path.join(dir, filename_force), delimiter=',', skip_header=skip_header, dtype=str)

    if Tests and exp < 3:
        timestep, force, displacement = data[:, 0], data[:, 1], data[:, 3]
    else:
        force, displacement = data[:, 0], data[:, 2]
        timestep = np.arange(len(force))

    dic_exp = {
        'timestep': timestep.astype(float),
        'force': force.astype(float),
        'displacement': displacement.astype(float)
    }
        

    if Tests:
        
        dic_dim = {'exp': data_dim[:, 0].astype(float), 
                    'lengths': data_dim[:, 1].astype(float), 
                    'lengths_fract': data_dim[:, 2].astype(float),
                    'width': data_dim[:, 3].astype(float), 
                    'thickness': data_dim[:, 4].astype(float)}
        
    else:
        
            
        lb_tot = np.zeros(len(data_dim[:, 0]))
        for i, lb in enumerate(data_dim[:, 3]):
            if lb != 'nan':
                fract_lb = eval(lb)
                lb_tot[i] = float(fract_lb)
            else:
                lb_tot[i] = lb
            
        dic_dim = {'exp': data_dim[:, 0].astype(float), 
                    'type':data_dim[:, 1], 
                    'lengths': data_dim[:, 2].astype(float), 
                    'lengths_fract': lb_tot, 
                    'width': data_dim[:, 4].astype(float), 
                    'thickness': data_dim[:, 5].astype(float), 
                    'x':data_dim[:, 6].astype(float), 
                    'y':data_dim[:, 7].astype(float), 
                    't':data_dim[:,8]}
        
        if (Floe == True) and (Temperature == False): 
            dic_dim.update({'loc': data_dim[:, 9]})
            
        if (Floe == False) and (Temperature == True): 
            dic_dim.update({'Temp': data_dim[:, 9]})
        
    
        if (Temperature) and (Floe):
            dic_dim.update({'Temp': data_dim[:, 9].astype(float),
                                'loc': data_dim[:, 10]})
        
    return dic_exp, dic_dim

def extract_data(dir_files, data_files, file_dim, Floe, Temp, f1 = 10, f2 = 100, unc_dim = 0.3/100, unc_force = 0.1):
    
    flexural_strength = np.zeros(len(data_files))
    unc_flexural_strength = np.zeros(len(data_files))
    volume_beams = np.zeros(len(data_files))
    experiments = np.arange(0, len(data_files))
    flexural_strength_buoyancy = np.zeros(len(data_files))
    force_experiments = []
    time_experiments = []
    
    flexural_strength_cantilever  = np.empty(0)
    flexural_strength_cantilever_buoyancy = np.empty(0)
    flexural_strength_threepoint = np.empty(0)
    unc_flexural_strength_threepoint = np.empty(0)
    
    _, dic_dim = read_data(dir_files, data_files[0], file_dim, 1, Floe = Floe, Temperature=Temp )
    lengths = dic_dim["lengths"]
    lb = dic_dim["lengths_fract"]
    width = dic_dim["width"]
    thickness = dic_dim['thickness']
    types_exp = dic_dim['type']
    x_loc = dic_dim['x']
    
    if Temp:
        temperature = dic_dim['Temp']
    if Floe:
        loc = dic_dim['loc']
    
    for exp, file in enumerate(data_files):
        
        dic_exp, dic_dim = read_data(dir_files, file, file_dim, exp)
        
        force_exp = dic_exp['force']
        time_exp = dic_exp['timestep']*1/f2
        
        length_exp, lb_exp, width_exp, thickness_exp = \
            lengths[exp]/100, lb[exp]/100, width[exp]/100, thickness[exp]/100
        # print('Maximum',  max_force)
        volume_beams[exp] = length_exp*width_exp*thickness_exp
        
        if types_exp[exp] == 'cant':
            max_force= np.max(force_exp)
            flexural_strength[exp], unc_flexural_strength[exp] = \
                me.cantilever(max_force, lb_exp, width_exp, thickness_exp,unc_dim,unc_force, uncertainty=True )
            flexural_strength_cantilever = np.append(flexural_strength_cantilever, flexural_strength[exp])
            
            flexural_strength_buoyancy[exp] = me.sigmaf_buoyancyCanti(max_force, lb_exp, width_exp, thickness_exp, me.ElasticModulus)
            flexural_strength_cantilever_buoyancy = np.append(flexural_strength_cantilever_buoyancy, flexural_strength_buoyancy[exp])
            # print(flexural_strength_buoyancy[exp])
                
        elif types_exp[exp] == '3pt':
            max_force, idx_force = me.maxforce_3point(force_exp, time_exp)
            flexural_strength[exp], unc_flexural_strength[exp] = \
                me.threepointbending(max_force, length_exp, width_exp, thickness_exp, unc_dim,unc_force, uncertainty=True)
            flexural_strength_threepoint = np.append(flexural_strength_threepoint, flexural_strength[exp])
            unc_flexural_strength_threepoint = np.append(unc_flexural_strength_threepoint, unc_flexural_strength[exp])
            
            flexural_strength_buoyancy[exp], _ = me.threepointbending(max_force, length_exp, width_exp, thickness_exp, unc_dim,unc_force, uncertainty=True)
        
        force_experiments.append(force_exp)
        time_experiments.append(time_exp)
        
    return force_experiments, flexural_strength, unc_flexural_strength, \
            volume_beams, experiments, time_experiments, flexural_strength_buoyancy, \
            flexural_strength_threepoint, flexural_strength_cantilever, flexural_strength_cantilever_buoyancy
  
#------ For the first Tests made on the 20250130 --------#
data_files_test = ['TEST_20250130_CANTILEVER_1_BY_BEACH.csv',
            'TEST_20250130_CANTILEVER_2_LEFT_ONE.csv',     
            'TEST_20250130_CANTILEVER_3_BY_WAVEMAKER.csv', 
            'TEST_20250130_CANTILEVER_4_RIGHT_THREE.CSV',  
            'TEST_20250130_CANTILEVER_5_FRONT_TWO.CSV',    
            'TEST_20250130_CANTILEVER_6_RIGHT_FOUR.CSV',   
            'TEST_20250130_CANTILEVER_7_FRONT_THREE.CSV',  
            'TEST_20250130_CANTILEVER_8_IN_MIDDLE.CSV']

file_dim_tests = 'dimensions_plates.txt'
dir_test30012025 = "/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/Preliminary_Exp_30012025/"

#------ For the tests on the unbroken-up ice for 04/02/2025 --------#
data_files_04022025 = ['20240205_1_cantilever.CSV',
            '20240205_2_3points.CSV',     
            '20240205_3_cantilever.CSV', 
            '20240205_4_3points.CSV', 
            '20240205_5_cantilever.CSV', 
            '20240205_6_3points.CSV']

file_dim_04022025 = '20250204_FSTD_Bending.txt'
dir_04022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250204_Felix/'
Floe_04022025  = False
Temperature_04022025  = False
#------ For the tests on the broken-up ice for 05/02/2025 --------#
data_files_05022025 = []
for i in range(1, 31):
    data_files_05022025.append('20240205_{}_3points.CSV'.format(i))
    
file_dim_05022025 = '20250205_FSTD_Bending.txt'
dir_05022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250205_Felix/'
Floe_05022025  = True
Temperature_05022025  = False


#------ For the tests on the unbroken-up ice for 06/02/2025 --------#
data_files_06022025 = ['20250206_1_3points.CSV',
            '20250206_2_cantilever.CSV',     
            '20250206_3_3points.CSV', 
            '20250206_4_cantilever.CSV', 
            '20250206_5_3points.CSV', 
            '20250206_6_cantilever.CSV']

file_dim_06022025 = '20250206_FSTD_Bending.txt'
dir_06022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250206_Felix/'
Floe_06022025  = False
Temperature_06022025  = True

#------ For the tests on the broken-up ice for 07/02/2025 --------#
data_files_07022025 = []
for i in range(1, 35):
    data_files_07022025.append('20250207_{}_3points.CSV'.format(i))
    
file_dim_07022025 = '20250207_FSTD_Bending.txt'
dir_07022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250207_Felix/'
Floe_07022025  = True
Temperature_07022025  = True


#------ For the tests on the unbroken-up ice for 12/02/2025 --------#

data_files_12022025 = ['20250212_1_cantilever.CSV',
            '20250212_2_3points.CSV',     
            '20250212_3_cantilever.CSV', 
            '20250212_4_3points.CSV', 
            '20250212_5_cantilever.CSV', 
            '20250212_6_3points.CSV']

file_dim_12022025 = '20250212_FSTD_Bending.txt'
dir_12022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250212_Felix/'
Floe_12022025  = False
Temperature_12022025  = True

#------ For the tests on the unbroken-up ice for 13/02/2025 --------#

data_files_13022025 = ['20250213_1_3points.CSV',
            '20250213_2_3points.CSV',     
            '20250213_3_3points.CSV', 
            '20250213_4_3points.CSV', 
            '20250213_5_3points.CSV', 
            '20250213_6_3points.CSV']

file_dim_13022025 = '20250213_FSTD_Bending.txt'
dir_13022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250213_Felix/'
Floe_13022025  = False
Temperature_13022025  = True

LittData_FlexStrength_Laboratory = {'flexural':np.array([1805.9, 
                                                2169.3, 
                                                1254.7, 
                                                2025.9, 
                                                2047, 
                                                2810.5, 
                                                1226.6, 
                                                867.9, 
                                                1411.5, 
                                                1715.1]), 
                                    'unc_flexural':np.array([97, 
                                                    999.6, 
                                                    561.8, 
                                                    444.2, 
                                                    486.6, 
                                                    1347.5, 
                                                    486.9, 
                                                    867.9, 
                                                    479.5, 
                                                    340.4])
}
    
    
    
    
    
    
    
