import os
import numpy as np
import sys
import scatlib
import utils
from netCDF4 import Dataset

raw_path = 'testing/Raw_Canonical/scan/'
proc_path = 'testing/Raw_nc/'

files = os.listdir(raw_path)
files

for filename in files:

    if 'KA-SCAT' in filename:
        iscat = 2
    elif 'KU-SCAT' in filename:
        iscat = 1
    else:
        iscat = 0

    if iscat > 0:
            
        configvars = scatlib.read_configuration(iscat)
        
        configvars["raw_data_path"] = raw_path
        configvars["processed_data_path"] = proc_path
        # configvars["raw_data_path"] = sys.argv[1]
        # configvars["processed_data_path"] = sys.argv[2]
        
        instrument_name = configvars["instrument_name"]
        calfile = configvars["calfile"]    #pass this as plain variable since it may get modified if creating a new calfile
        raw_data_path = configvars["raw_data_path"]
        processed_data_path = configvars["processed_data_path"]
    
        try:
            ## READ_HEADER
            
            header_output = scatlib.read_header(raw_path+filename, raw_data_path, configvars)
    
            # rcw get the reference_calibration_loop_power_file         
            reference_calibration_loop_power_file = 10**(header_output[1]["cal_peak_dbm"]/10.)  
    
            ## READ_RAW
    
            raw_output =  scatlib.read_raw(configvars, header_output[0],raw_path+filename,
                                                     header_output[3], header_output[4])
    
            utils.write_nc(configvars,filename,raw_output,header_output)
    
        except Exception as e:
            print('FAILURE')
            print(filename)
            print(e)