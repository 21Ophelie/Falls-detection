import matplotlib.pyplot as plt
import db 

# this file is used to show the graphique of the value of the accelertion rate or the heart rate

# to show the heart rate values :

#nb = 30*5  # number of value that you want to see
#hr=db.getvalues(nb,'HR',0)
#hrval = hr[:nb-1]  # the values
#hrtime = hr[nb:2*nb-1] # the times of the measurements
#plt.title("heart rate measurements")
#plt.plot( hrtime, hrval)
#plt.xlabel('second')
#plt.ylabel('bpm')
#plt.show()

#print('min: ',min(hrval)[0],'  max : ', max(hrval)[0] , 'dif:',max(hrval)[0]-min(hrval)[0])  # to see the difference between the min and the max value
#db.addgaptodb('hr',max(hrval)[0]-min(hrval)[0])  # to add the gap in the table gap


# to show the acceleration rate values :

nb=42*50 # there are 50 values per second
acc=db.getvalues(nb,'Acc',0)
accval = acc[:nb-1]
acctime =acc[nb:nb*2-1]
accz=acc[nb*2:nb*3-1]
plt.title("acceleration rate measurements on xyz")
plt.plot(acctime, accval)
#plt.plot(acctime, accval)
plt.xlabel('second')
plt.ylabel('mg')
plt.show()


plt.title("acceleration rate measurements on z")
plt.plot(acctime, accz)
#plt.plot(acctime, accz)
plt.xlabel('second')
plt.ylabel('mg')
plt.show()


print('minz: ',min(accz)[0],'	max : ', max(accz)[0] , 'dif:',max(accz)[0]-min(accz)[0])  # to see the difference between the min and the max value of the module
print('min: ',min(accval)[0],'  max : ', max(accval)[0] , 'dif:',max(accval)[0]-min(accval)[0]) # to see the difference between the min and the max value of the z axis
print('mint: ',min(acctime)[0],'  max : ', max(acctime)[0] , 'dif:',max(acctime)[0]-min(acctime)[0]) # to see the time between the first and the last value

#db.addgaptodb('acc',max(accval)[0]-min(accval)[0]) # adding the gap in the table gap

