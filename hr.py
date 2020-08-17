
import struct
from bluepy.btle import *
from db import *
import time

# the mac address of the polar OH1+ and the name of its heart rate characteristic 
address="A0:9E:1A:55:80:02"
characteristic='00002a37-0000-1000-8000-00805f9b34fb'

# the notify handle value that is used to access to the heart rate's value 
notify_handle=41

# callback class
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

  # this function is called each time we read the notification of the heart rate
    def handleNotification(self, cHandle, data):

       # to convert the value of the heart rate
        data = bytearray(data)
       #adds the value in the database
        addhrtodb(data[1])
        print("hr : ",data[1])

# this function is called at the begining of the principal main to get the notify handle value
def init_notify_handle_hr():
    global notify_handle
    per = Peripheral(address,"public")
    try:
    	print("trying to connect the heart rate device")
    	per.setDelegate(MyDelegate())
    	notify = per.getCharacteristics(uuid=characteristic)[0]
    	notify_handle = notify.getHandle() + 1
    	print("heart rate device connected")

    finally:
        per.disconnect()


#this function is called in the function gethr() to enable the access of the heart rate value
def enable_notify(per,  chara_uuid):
    setup_data = b"\x01\x00"
    #notify = per.getCharacteristics(uuid=chara_uuid)[0]
    #notify_handle = notify.getHandle() + 1
    #notify_handle = 41 
    per.writeCharacteristic(notify_handle, setup_data, withResponse=True)

# this function is called in the main file (thread2.py) to get the value of the heart rate
def gethr():
	
	#tmps1=time.time()
	#print(tmps1)
	# connect to device
	per = Peripheral(address,"public")
		
	try:
    		# set callback for notifications
		
		per.setDelegate(MyDelegate())
	
		enable_notify(per,characteristic)
	
    		# wait for answer
		#for x in range (1) :
		#	if per.waitForNotifications(0.5):
		#		continue		
		per.waitForNotifications(1.0)
		#tmps=time.time()
		#print(tmps)
		#print("time : ", tmps-tmps1)
	finally:
		per.disconnect()
	

#gethr()
