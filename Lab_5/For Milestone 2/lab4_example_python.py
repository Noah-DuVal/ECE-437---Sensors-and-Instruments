# -*- coding: utf-8 -*-

#%%
# import various libraries necessary to run your Python code
import time   # time related library
import sys,os    # system related library
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
# Define the two variables that will send data to the FPGA
# We will use WireIn instructions to send data to the FPGA
 # send a "go" signal to the FSM
 
  # Update the WireIns

#%% 
# Since we are using a slow clock on the FPGA to compute the results
# we need to wait for the result to be computed
time.sleep(1)                 
avg = 0
 # send a "stop" signal to the FSM
for i in range(10):
    dev.SetWireInValue(0x00, 1)
    print("Send GO signal to the FSM") 
    time.sleep(0.5) 
    dev.UpdateWireIns()  # Update the WireIns
    print("Send STOP signal to the FSM")
    dev.UpdateWireOuts()
    result = dev.GetWireOutValue(0x21)/128
    print(str(result))
    dev.SetWireInValue(0x00, 0)
    dev.UpdateWireIns()
print("Average over 10 runs is: " + str(avg/10))
dev
dev
dev.Close
    
#%%