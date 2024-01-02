# NOTE 1
# If your power supply goes into an error state (i.e., the word
# error is printed on the front of the device), use this command
# power_supply.write("*CLS")
# to clear the error so that you can rerun your code. The supply
# typically beeps after an error has occured.
#%% This section does the connection to the devices as well as sets up the OKC control
import pyvisa as visa
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time
import sys,os
mpl.style.use('ggplot')
ok_sdk_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\Python\\x64"
ok_dll_loc = "C:\\Program Files\\Opal Kelly\\FrontPanelUSB\\API\\lib\\x64"
sys.path.append(ok_sdk_loc) # add the path of the OK library
os.add_dll_directory(ok_dll_loc)
import ok # OpalKelly library
# load the bit file in the FPGA
dev = ok.okCFrontPanel() # define a device for FrontPanel communication
SerialStatus=dev.OpenBySerial("") # open USB communication with the OK board
ConfigStatus=dev.ConfigureFPGA("lab2_example.bit"); #load the bit file

# Check if FrontPanel is initialized correctly and if the bit file is loaded.
# Otherwise terminate the program
print("----------------------------------------------------")
if SerialStatus == 0:
    print ("FrontPanel host interface was successfully initialized.")
else:
    print ("FrontPanel host interface not detected. The error code number is:" + str(int(SerialStatus)))
    print("Exiting the program.")
    sys.exit ()
if ConfigStatus == 0:
    print ("Your bit file is successfully loaded in the FPGA.")
else:
    print ("Your bit file did not load. The error code number is:" + str(int(ConfigStatus)))
    print ("Exiting the progam.")
    sys.exit ()
print("----------------------------------------------------")
print("----------------------------------------------------")


#%% This part of the code does the setup for the powersupply
#%%
# This section of the code cycles through all USB connected devices to the computer.
# The code figures out the USB port number for each instrument.
# The port number for each instrument is stored in a variable named “instrument_id”
# If the instrument is turned off or if you are trying to connect to the 
# keyboard or mouse, you will get a message that you cannot connect on that port.
device_manager = visa.ResourceManager()
devices = device_manager.list_resources()
number_of_device = len(devices)

power_supply_id = -1;
waveform_generator_id = -1;
digital_multimeter_id = -1;
oscilloscope_id = -1;

# assumes only the DC power supply is connected
for i in range (0, number_of_device):

# check that it is actually the power supply
    try:
        device_temp = device_manager.open_resource(devices[i])
        print("Instrument connect on USB port number [" + str(i) + "] is " + device_temp.query("*IDN?"))
        if (device_temp.query("*IDN?") == 'HEWLETT-PACKARD,E3631A,0,3.2-6.0-2.0\r\n'):
            power_supply_id = i        
        if (device_temp.query("*IDN?") == 'HEWLETT-PACKARD,E3631A,0,3.0-6.0-2.0\r\n'):
            power_supply_id = i
        if (device_temp.query("*IDN?") == 'Agilent Technologies,33511B,MY52301259,3.03-1.19-2.00-52-00\n'):
            waveform_generator_id = i
        if (device_temp.query("*IDN?") == 'Agilent Technologies,34461A,MY53207926,A.01.10-02.25-01.10-00.35-01-01\n'):
            digital_multimeter_id = i 
        if (device_temp.query("*IDN?") == 'Keysight Technologies,34461A,MY53212931,A.02.08-02.37-02.08-00.49-01-01\n'):
            digital_multimeter_id = i            
        if (device_temp.query("*IDN?") == 'KEYSIGHT TECHNOLOGIES,MSO-X 3024T,MY54440281,07.10.2017042905\n'):
            oscilloscope_id = i                        
        device_temp.close()
    except:
        print("Instrument on USB port number [" + str(i) + "] cannot be connected. The instrument might be powered of or you are trying to connect to a mouse or keyboard.\n")
    

#%%
# Open the USB communication port with the power supply.
# The power supply is connected on USB port number power_supply_id.
# If the power supply ss not connected or turned off, the program will exit.
# Otherwise, the power_supply variable is the handler to the power supply
    
if (power_supply_id == -1):
    print("Power supply instrument is not powered on or connected to the PC.")    
else:
    print("Power supply is connected to the PC.")
    power_supply = device_manager.open_resource(devices[power_supply_id]) 
    
#%% This part is for the actual test-benching
    #we setup the max_voltage and the step size.
    steps = 10
    max_volt = 4.75
    output_voltage = np.arange(0, max_volt, max_volt/steps)
    measured_voltage = np.array([],[]) # create an empty list to hold our values
    measured_current = np.array([],[]) # create an empty list to hold our values
    measured_power = np.array([],[])
    measured_voltage_std = np.array([])
    measured_voltage_avg = np.array([])
    measured_current_std = np.array([])
    measured_current_avg = np.array([])
    measured_power_std = np.array([])
    measured_power_avg = np.array([])
    
    print(power_supply.write("OUTPUT ON")) # power supply output is turned on

    # loop through the different voltages we will apply to the power supply
    # For each voltage applied on the power supply, 
    # measure the voltage and current supplied by the 6V power supply
    for v in output_voltage:
        # apply the desired voltage on teh 6V power supply and limist the output current to 0.5A
        power_supply.write("APPLy P6V, %0.2f, 0.5" % v)
    
        # pause 50ms to let things settle
        time.sleep(0.5)
        
        # read the output voltage on the 6V power supply
        for i in range(20):
            
            measured_voltage_tmp = power_supply.query("MEASure:VOLTage:DC? P6V")
            measured_voltage[v][i] = measured_voltage_tmp
            time.sleep(0.125)
            # read the output current on the 6V power supply
            measured_current_tmp = power_supply.query("MEASure:CURRent:DC? P6V")
            measured_current[v][i] = measured_current_tmp
            #formulate the output power
            measured_power_tmp = measured_current_tmp*measured_voltage_tmp
            measured_power[v][i] =  measured_power_tmp
    # power supply output is turned off
    print(power_supply.write("OUTPUT OFF"))
    # close the power supply USB handler.
    # Otherwise you cannot connect to it in the future
    power_supply.close()

#%% Plot measured data. First convert the data from strings to numbers (ie floats)
    voltage_list=np.zeros(np.size(output_voltage))
    current_list=np.zeros(np.size(output_voltage))
    power_list = np.zeros(np.size(output_voltage))
    for i in range(len(measured_voltage)):
        #calculate mean and stdev for voltage
        measured_voltage_avg[i] = np.mean(measured_voltage[i][0:20])
        measured_voltage_std[i] = np.std(measured_voltage[i][0:20])
        #calculate mean and stdev for current
        measured_current_avg[i] = np.mean(measured_current[i][0:20])
        measured_current_std[i] = np.std(measured_current[i][0:20])
        #calculate mean and stdev for power
        measured_power_avg[i] = np.mean(measured_power[i][0:20])
        measured_power_std[i] = np.mean(measured_power[i][0:20])
   
    # plot results (applied voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_voltage_avg)
    plt.title("Supplied Voltage vs. Measured Voltage Average")
    plt.xlabel("Applied Volts [V]")
    plt.ylabel("Measured Voltage Average")
    plt.draw()
    # plot results (measured voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_voltage_std)
    plt.title("Supplied Voltage vs. Measured Voltage Std. Dev.")
    plt.xlabel("Supplied Volts [V]")
    plt.ylabel("Measured Voltage Std. Dev.")
    plt.draw()
    # plot results (applied voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_current_avg)
    plt.title("Supplied Voltage vs. Measured Current Average")
    plt.xlabel("Applied Volts [V]")
    plt.ylabel("Measured Current Average")
    plt.draw()
    # plot results (measured voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_current_std)
    plt.title("Supplied Voltage vs. Measured Current Std. Dev.")
    plt.xlabel("Supplied Volts [V]")
    plt.ylabel("Measured Current Std. Dev.")
    plt.draw()
    # plot results (applied voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_power_avg)
    plt.title("Supplied Voltage vs. Measured Power Average")
    plt.xlabel("Applied Volts [V]")
    plt.ylabel("Measured Power Average")
    plt.draw()
    # plot results (measured voltage vs measured supplied current)
    plt.figure()
    plt.plot(output_voltage,measured_power_std)
    plt.title("Supplied Voltage vs. Measured Power Std. Dev.")
    plt.xlabel("Supplied Volts [V]")
    plt.ylabel("Measured Power Std. Dev.")
    plt.draw()
    # show all plots
    plt.show()
