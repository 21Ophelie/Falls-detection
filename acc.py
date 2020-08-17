import struct
from bluepy.btle import *
from db import *
import ctypes
import math
import time

# the mac address of the bbc micro bit and the name of its acceleration rate characteristic 
address = "F4:11:5F:12:80:B1"
characteristic = 'e95dca4b-251d-470a-a062-fa1922dfa9a8'

# the notify handle value that is used to access to the acceleration rate's value 
notify_handle = 40


# callback class
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # this function is called each time we read the notification of the acceleration rate
    def handleNotification(self, cHandle, data):
        
	# the data of the acceleration is in bytes so we need to convert
        # there are 2 bytes per dimension (x, y, z)

	high_x = (data[1])<<8
        low_x = data[0]
        x = high_x | low_x
        x = ctypes.c_short(x).value 
         
        high_y = (data[3])<<8
        low_y = data[2]
        y = high_y | low_y
        y = ctypes.c_short(y).value 
        
        high_z = (data[5])<<8
        low_z = data[4]
        z = high_z | low_z
        z = ctypes.c_short(z).value 
	
	#calculate the module of the acceleration rate
        acceleration = math.sqrt(x**2 + y**2 + z**2)
        #print("x=",x," y=",y," z=",z," acc=",acceleration) 
        
	# adds the values in the database
        addacctodb(acceleration,z)

# this function is called at the begining of the principal main to get the notify handle value
def init_notify_handle_acc():
    global notify_handle
    # connect to device (the bbc micro bit)
    per = Peripheral(address,ADDR_TYPE_RANDOM)
    try:
    	print("trying to connect the acceleration rate device and get the notify handle")
    	per.setDelegate(MyDelegate())
    	notify = per.getCharacteristics(uuid=characteristic)[0]
    	notify_handle = notify.getHandle() + 1
    	print("notify handle of the acceleration rate : ", notify_handle)

    finally:
        per.disconnect()

#this function is called to enable the access of the acceleration value
def enable_notify(per,  chara_uuid):
    setup_data = b"\x01\x00"

    #notify = per.getCharacteristics(uuid=chara_uuid)[0]
    #notify_handle = notify.getHandle() + 1

    #notify_handle = 40

    per.writeCharacteristic(notify_handle, setup_data, withResponse=True)

# this function is called in the main file (thread2.py) to get the value of the acceleration rate
def getacc():
    # connect to device (the bbc micro bit)
    per = Peripheral(address,ADDR_TYPE_RANDOM)
    try:
             
        #per.setSecurityLevel("medium")
        per.setDelegate(MyDelegate())
                          
        # enable notification
        enable_notify(per,  characteristic)
       
        #tmps1=time.time()
        
	# the bbc micro bit sends 50 notifications per second, each notification contain the value of the acceleration on each dimension
	# the function waitForNotifications() called the function handleNotification() of the class MyDelegate
        for x in range (50) :
        	if per.waitForNotifications(0.2):
        		continue
       
                
        #tmps=time.time()
        
        #print("time : ", tmps-tmps1)
    finally:
        per.disconnect()
        
#getacc()
