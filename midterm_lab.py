
# -*- coding: utf-8 -*-

#%%
# import various libraries necessary to run your Python code
import time   # time related library
import sys,os    # system related library
import numpy as np
ok_sdk_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\Python\\x64"
ok_dll_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\lib\\x64"

sys.path.append(ok_sdk_loc)   # add the path of the OK library
os.add_dll_directory(ok_dll_loc)

import ok     # OpalKelly library

#%% 
# Define FrontPanel device variable, open USB communication and
# load the bit file in the FPGA
dev = ok.okCFrontPanel()  # define a device for FrontPanel communication
SerialStatus=dev.OpenBySerial("")      # open USB communication with the OK board
# We will NOT load the bit file because it will be loaded using JTAG interface from Vivado

# Check if FrontPanel is initialized correctly and if the bit file is loaded.
# Otherwise terminate the program
print("----------------------------------------------------")
if SerialStatus == 0:
    print ("FrontPanel host interface was successfully initialized.")
else:    
    print ("FrontPanel host interface not detected. The error code number is:" + str(int(SerialStatus)))
    print("Exiting the program.")
    sys.exit ()


#%% 


#%% 
# Since we are using a slow clock on the FPGA to compute the results
# we need to wait for the result to be computed
#0 is a write, 1 is a read

#address 6 was made to be PC_control because we were trying some things.

#this is where we begin writing to the registers to enable both the Gyroscope and the Accelerometer
dev.SetWireInValue(0x01,1) #we only need one to write
dev.SetWireInValue(0x02,1)#perform a write(0) or read(1)
dev.SetWireInValue(0x03,87)#perform input 8'b010101111 to register
dev.SetWireInValue(0x05,50)#write to this dev_addr
dev.SetWireInValue(0x04,32)#write  to this sub_addr
dev.UpdateWireIns()
dev.SetWireInValue(0x00,1)
dev.UpdateWireIns();
dev.SetWireInValue(0x00,0)
dev.UpdateWireIns();
dev.UpdateWireOuts();
print(dev.GetWireOutValue(0x21))


dev
dev
dev.Close
    
#%%