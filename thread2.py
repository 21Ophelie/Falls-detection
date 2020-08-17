import threading
import time
from hr import *
from acc import *
from db import *
import polly

exitFlag = 0

verrou = threading.RLock()

class myThreadHR (threading.Thread):
   def __init__(self, threadID, name, counter,delay):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.delay = delay
   def run(self):
      print ("Starting " + self.name)
      getseveralhr(self.name,self.counter,self.delay)
      print ("Exiting " + self.name)

class myThreadAcc (threading.Thread):
   def __init__(self, threadID, name, counter,delay):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.delay = delay
   def run(self):
      print ("Starting " + self.name)
      getseveralacc(self.name, self.counter, self.delay)
      print ("Exiting " + self.name)

class myThreadMoy (threading.Thread):
   def __init__(self, threadID, name, counter,delay,wait):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
      self.delay = delay
      self.wait = wait
   def run(self):
      print ("Starting " + self.name)
      getmoy(self.name, self.counter,self.delay, self.wait)
      print ("Exiting " + self.name)

def getmoy (threadName,counter, delay,wait):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      
      if accdiff("Acc",75, 2200,"z",wait*50)==1:
      	print("step1")
      	#if accdiff("Acc",1250,200,val,0)==1:
      	if accenergie("Acc",wait*50,4000000)==1:
      		print("step2")
      		if moylast("HR",600,5,wait+2-5,-100,"val")==1:
      			print("step3")
      			polly.play()
      #print(counter)
      counter -= 1


def getseveralhr (threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      #time.sleep(delay)
      gethr()
      #print(counter)
      counter -= 1

def getseveralacc (threadName, counter,delay):
   while counter:
      if exitFlag:
         threadName.exit()
      #time.sleep(delay)
      getacc()
      #energie("Acc",50)
      print("acc:",counter)
      counter -= 1

# to get the notify handle value to acces to the measurements of the devices
init_notify_handle_acc()
init_notify_handle_hr()
#create voice file 
polly.createall()
#create tables in the database
createtables()
# Create new threads
it= 200
thread1 = myThreadAcc(1, "acc",it,0) #threadID, name, counter,delay
thread2 = myThreadHR(2, "hr", it,0) #threadID, name, counter,delay
thread3 = myThreadMoy(3, "moy",400,0.6,15) #threadID, name, counter,delay,wait


# Start new Threads
#addaccstodb(0,0,1250)
thread1.start()
thread2.start()
thread3.start()
thread1.join()
thread2.join()
thread3.join()
print ("Exiting Main Thread")
