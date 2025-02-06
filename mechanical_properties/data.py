import numpy as np

def read_data(dir, filename_force, filename_dim, exp, Tests = False):
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
    data_dim = np.loadtxt(dir + filename_dim, skiprows=1, delimiter=',',dtype = float)
    
    if (Tests and exp < 3):
        data = np.genfromtxt(dir + filename_force, delimiter=',', skip_header=7, dtype = str)
        
        timestep = data[:, 0]
        force = data[:, 1]
        displacement = data[:, 3]
    
    else:
        data = np.genfromtxt(dir + filename_force, delimiter=',', skip_header=2, dtype = str)
        
        force = data[:, 0]
        displacement = data[:, 2]
        timestep = np.arange(0, len(force))
        
    dic_exp = {'timestep': timestep.astype(float), 'force': force.astype(float), \
        'displacement': displacement.astype(float)}
        

    if Tests:
        
        dic_dim = {'exp': data_dim[:, 0], 'lengths': data_dim[:, 1], 'lengths_fract': data_dim[:, 2], \
                'width': data_dim[:, 3], 'thickness': data_dim[:, 4]}
    
    else:
        dic_dim = {'exp': data_dim[:, 0], 'type':data_dim[:, 1], 'lengths': data_dim[:, 2], 'lengths_fract': data_dim[:, 3], \
                'width': data_dim[:, 4], 'thickness': data_dim[:, 5], 'x':data_dim[:, 6], 'y':data_dim[:, 7], 't':data_dim[:,8]}

    return dic_exp, dic_dim



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

file_dim_04022025 = '20250204_FSTD_Bending.txt.txt'
dir_04022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250204_Felix/'

#------ For the tests on the broken-up ice for 05/02/2025 --------#
data_files_05022025 = []
for i in range(1, 31):
    data_files_05022025.append('20240205_{}_3points.CSV'.format(i))
    
file_dim_05022025 = '20250205_FSTD_Bending.txt'
dir_05022025      = '/aos/home/fstdenis/ICE_TANK/mechanical_properties/Experiments/20250205_Felix/'
