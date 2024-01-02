# -*- coding: utf-8 -*-
#%%
# import various libraries necessary to run your Python code
import time # time related library
import sys,os # system related library
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.style.use('ggplot')
ok_sdk_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\Python\\x64"
ok_dll_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\lib\\x64"
sys.path.append(ok_sdk_loc) # add the path of the OK library
os.add_dll_directory(ok_dll_loc)
import ok # OpalKelly library
#%%
# Define FrontPanel device variable, open USB communication and
# load the bit file in the FPGA
dev = ok.okCFrontPanel() # define a device for FrontPanel communication
SerialStatus=dev.OpenBySerial("") # open USB communication with the OK board
# We will NOT load the bit file because it will be loaded using JTAG interface from Vivado
# Check if FrontPanel is initialized correctly and if the bit file is loaded.
# Otherwise terminate the program
print("----------------------------------------------------")
if SerialStatus == 0:
    print ("FrontPanel host interface was successfully initialized.")
else:
    print ("FrontPanel host interface not detected. The error code number is:" +
    str(int(SerialStatus)))
    print("Exiting the program.")
    sys.exit ()
#%%

#%%
# Since we are using a slow clock on the FPGA to compute the results
# we need to wait for the result to be computed
#0 is a write, 1 is a read
#address 6 was made to be PC_control because we were trying some things.
#this is where we begin writing to the registers to enable both the Gyroscope and the
#Accelerometer
#%%
#Addresses for OK
trigger = 0x00;
dev_addr = 0x01;
sub_addr = 0x02;
data_in = 0x03;
d_out_1 = 0x20;
d_out_2 = 0x21;
d_out_3 = 0x22;
d_out_4 = 0x23;
d_out_5 = 0x24;
d_out_6 = 0x25;
#%%
#The functions needed
def get_accel_data(dev):
    time.sleep(.01)
    dev.SetWireInValue(dev_addr, 0x32)
    dev.SetWireInValue(sub_addr, 0xA8)

    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 1)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 0)
    dev.UpdateWireIns()
    dev.UpdateWireOuts()
    X_L_A = dev.GetWireOutValue(d_out_1)
    X_H_A = dev.GetWireOutValue(d_out_2)
    Y_L_A = dev.GetWireOutValue(d_out_3)
    Y_H_A = dev.GetWireOutValue(d_out_4)
    Z_L_A = dev.GetWireOutValue(d_out_5)
    Z_H_A = dev.GetWireOutValue(d_out_6)
    X = twobit(X_L_A,X_H_A)/16*0.001
    Y = twobit(Y_L_A,Y_H_A)/16*0.001
    Z = twobit(Z_L_A,Z_H_A)/16*0.001
    
    return X,Y,Z
    
def twobit(m1, m2):
    val_x = (bin(m1 + (m2 << 8)))
    if((int(val_x, 2) >> 15)):
        val_x = int(val_x, 2) - (1<<16)
    else:
        val_x = int(val_x, 2)
    return val_x

def get_mag_data(dev):
    time.sleep(0.001)
    dev.SetWireInValue(dev_addr, 0x3C)
    dev.SetWireInValue(sub_addr, 0b00000011)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 1)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 0)
    dev.UpdateWireIns()
    dev.UpdateWireOuts()
    X_H_A = dev.GetWireOutValue(d_out_1)
    X_L_A = dev.GetWireOutValue(d_out_2)
    Z_H_A = dev.GetWireOutValue(d_out_3)
    Z_L_A = dev.GetWireOutValue(d_out_4)
    Y_H_A = dev.GetWireOutValue(d_out_5)
    Y_L_A = dev.GetWireOutValue(d_out_6)
    X = twobit(X_H_A,X_L_A)/1000
    Y = twobit(Y_H_A,Y_L_A)/1000
    Z = twobit(Z_H_A,Z_L_A)/1000
    return X,Y,Z

def prog_i2c(dev):
    #program the accelerometer
    trigger = 0x00;
    dev_addr = 0x01;
    sub_addr = 0x02;
    data_in = 0x03;
    dev.SetWireInValue(dev_addr, 0x32)
    dev.SetWireInValue(sub_addr, 0x20)
    dev.SetWireInValue(data_in,  0b01110111)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 1)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 0)
    dev.UpdateWireIns()
    time.sleep(0.5)
    dev.SetWireInValue(dev_addr, 0x32)
    dev.SetWireInValue(sub_addr, 0x23)
    dev.SetWireInValue(data_in,  0b10000000)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 1)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 0)
    dev.UpdateWireIns()
    time.sleep(0.5)
    dev.SetWireInValue(dev_addr, 0x3C)
    dev.SetWireInValue(sub_addr, 0x02)
    dev.SetWireInValue(data_in,  0x00)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 1)
    dev.UpdateWireIns()
    dev.SetWireInValue(trigger, 0)
    dev.UpdateWireIns()
    return

prog_i2c(dev)
start = time.time()
while(1):
    X,Y,Z = get_accel_data(dev)
    print(X,Y,Z)
stop = time.time()
print(stop-start)
'''
dev.SetWireInValue(dev_addr, 0x32)
dev.SetWireInValue(sub_addr, 0x20)
dev.SetWireInValue(data_in,  0b01110111)
dev.UpdateWireIns()
dev.SetWireInValue(trigger, 1)
dev.UpdateWireIns()
dev.SetWireInValue(trigger, 0)
dev.UpdateWireIns()
dev.SetWireInValue(dev_addr, 0x32)
dev.SetWireInValue(sub_addr, 0xA8)

dev.UpdateWireIns()
dev.SetWireInValue(trigger, 1)
dev.UpdateWireIns()
dev.SetWireInValue(trigger, 0)
dev.UpdateWireIns()
dev.UpdateWireOuts()
X = dev.GetWireOutValue(d_out_1)
Y = dev.GetWireOutValue(d_out_2)
Z = dev.GetWireOutValue(d_out_3)
print(X,Y,Z)
'''
'''
def Use_Sensor(R_or_W, dev_addr, sub_addr, read_count, data, dev):
########### Writes the Contrl Reg ############################
    dev.SetWireInValue(0x01, read_count) #how many time to iterate
    dev.SetWireInValue(0x02, R_or_W) #Decides read or write
    dev.SetWireInValue(0x03, data) # Data to write
    dev.SetWireInValue(0x04, sub_addr) #Sets the Sub Adress
    dev.SetWireInValue(0x05, dev_addr) #Sets the Dev Adress
    dev.UpdateWireIns()
    dev.SetWireInValue(0x00,1) #Starts FSM
    dev.UpdateWireIns()
    dev.SetWireInValue(0x00,0) #Turns FSM Off
    dev.UpdateWireIns()
    dev.UpdateWireOuts()
    if(read_count == 1):
        addr = 0x21
    elif(read_count == 2):
        addr = 0x22
    elif(read_count == 3):
        addr = 0x23
    elif(read_count == 4):
        addr = 0x24
    elif(read_count == 5):
        addr = 0x25
    elif(read_count == 6):
        addr = 0x26
    else:
        return
    if (R_or_W == 1):
        x = dev.GetWireOutValue(addr)
        return x
    else:
        return
def twobit(m1, m2):
    val_x = (bin(m1 + (m2 << 8)))
    if((int(val_x, 2) >> 15)):
        val_x = int(val_x, 2) - (1<<16)
    else:
        val_x = int(val_x, 2)
    return val_x
#6 is direction and 7 is enable
'''
'''
dev.SetWireInValue(0x06,1)
dev.SetWireInValue(0x07,1)
dev.UpdateWireIns()
time.sleep(1)
dev.SetWireInValue(0x06,0)
dev.UpdateWireIns()
'''

'''
def Moveaccel(direction, time,dev):
    dev.SetWireInValue(0x07,0)
    dev.SetWireInValue(0x06,direction)
    dev.UpdateWireIns()
    
    dev.SetWireInValue(0x07,1)
    dev.UpdateWireIns()
    Use_Sensor(0, 0x32, 0x20, 1, 0x97, dev) #write to Lin Accell CTRL_REG_A 8'b01010111
    
    X_L_A = Use_Sensor(1, 0x33, 0x28, 1, 0, dev) #Reads Lin Al from X Low
    
    X_H_A = Use_Sensor(1, 0x33, 0x29, 2, 0, dev)
    
    Y_L_A = Use_Sensor(1, 0x33, 0x2A, 3, 0, dev)
    time.sleep(.1)
    Y_H_A = Use_Sensor(1, 0x33, 0x2B, 4, 0, dev)
    time.sleep(.1)
    Z_L_A = Use_Sensor(1, 0x33, 0x2C, 5, 0, dev)
    time.sleep(.1)
    Z_H_A = Use_Sensor(1, 0x33, 0x2D, 6, 0, dev)
    time.sleep(.1)
    X_A = twobit(X_L_A,X_H_A)/16384
    Y_A = twobit(Y_L_A,Y_H_A)/16384
    Z_A = twobit(Z_L_A,Z_H_A)/16384
    
    
    print(X_A,Y_A,Z_A)
    dev.SetWireInValue(0x07,0)
    dev.UpdateWireIns()
    
    
    return
'''

'''
def Movemag(direction, time,dev):
    dev.SetWireInValue(0x07,0)
    dev.SetWireInValue(0x06,direction)
    dev.UpdateWireIns()
    time.sleep(1)
    for i in range(5):
        
        dev.SetWireInValue(0x07,1)
        dev.UpdateWireIns()
        Use_Sensor(0, 0x3C, 0x02, 1, 0x00, dev)
        X_H_M = Use_Sensor(1, 0x3C, 0x03, 1, 0, dev) #Reads Mag Field X-Y-Z
        time.sleep(0.0007)
        X_L_M = Use_Sensor(1, 0x3C, 0x04, 2, 0, dev)
        time.sleep(0.0007)
        Z_H_M = Use_Sensor(1, 0x3C, 0x05, 3, 0, dev)
        time.sleep(0.0007)
        Z_L_M = Use_Sensor(1, 0x3C, 0x06, 4, 0, dev)
        time.sleep(0.0007)
        Y_H_M = Use_Sensor(1, 0x3C, 0x07, 5, 0, dev)
        time.sleep(0.0007)
        Y_L_M = Use_Sensor(1, 0x3C, 0x08, 6, 0, dev)
        X_A = twobit(X_L_M,X_H_M)/1000
        Y_A = twobit(Y_L_M,Y_H_M)/1000
        Z_A = twobit(Z_L_M,Z_H_M)/1000
        print(2*X_A, 2*Y_A, 2*Z_A)
        #print('Pulse: ' + str(i))
        
    dev.SetWireInValue(0x07,0)
    dev.UpdateWireIns()
    
    
    return
'''
'''
############### Getting Linear Accelleration ###############
Use_Sensor(0, 0x32, 0x20, 1, 0b01000111, dev) #write to Lin Accell CTRL_REG_A 8'b01010111
start = time.time()
while(1):
    
    X_L_A = Use_Sensor(1, 0x33, 0x28, 1, 0, dev) #Reads Lin Al from X Low
    time.sleep(.001)
    X_H_A = Use_Sensor(1, 0x33, 0x29, 2, 0, dev)
    time.sleep(.001)
    Y_L_A = Use_Sensor(1, 0x33, 0x2A, 3, 0, dev)
    time.sleep(.001)
    Y_H_A = Use_Sensor(1, 0x33, 0x2B, 4, 0, dev)
    time.sleep(.001)
    Z_L_A = Use_Sensor(1, 0x33, 0x2C, 5, 0, dev)
    time.sleep(.001)
    Z_H_A = Use_Sensor(1, 0x33, 0x2D, 6, 0, dev)
    time.sleep(.001)
    X_A = twobit(X_L_A,X_H_A)/16384
    Y_A = twobit(Y_L_A,Y_H_A)/16384
    Z_A = twobit(Z_L_A,Z_H_A)/16384
    print(X_A/2,Y_A/2,Z_A/2)
stop = time.time()    
print(stop-start)
    ############### Getting Magnetic Field ###################
'''
'''
while(1):
    Use_Sensor(0, 0x3C, 0x02, 1, 0x00, dev)
    time.sleep(0.5)
    X_H_M = Use_Sensor(1, 0x3C, 0x03, 1, 0, dev) #Reads Mag Field X-Y-Z
    time.sleep(.02)
    X_L_M = Use_Sensor(1, 0x3C, 0x04, 2, 0, dev)
    time.sleep(.02)
    Z_H_M = Use_Sensor(1, 0x3C, 0x05, 3, 0, dev)
    time.sleep(.02)
    Z_L_M = Use_Sensor(1, 0x3C, 0x06, 4, 0, dev)
    time.sleep(.02)
    Y_H_M = Use_Sensor(1, 0x3C, 0x07, 5, 0, dev)
    time.sleep(.02)
    Y_L_M = Use_Sensor(1, 0x3C, 0x08, 6, 0, dev)
    X_A = twobit(X_L_M,X_H_M)/1000
    Y_A = twobit(Y_L_M,Y_H_M)/1000
    Z_A = twobit(Z_L_M,Z_H_M)/1000
    print(X_A, Y_A, Z_A)
'''
dev
dev
dev.Close

#%%