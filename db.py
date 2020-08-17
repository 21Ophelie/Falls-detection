import mariadb
import sys

# database parameters
username = "username"
userpassword = "userpassword"
userdatabase = "falls"

#create the table measurements for storing the heart rate and the acceleration rate, and the table gap to store the the energy during 25 second or the gap of the acceleration rate during 1.5 second
def createtables():
   try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()
        cur.execute("create table if not exists measurements (id bigint auto_increment primary key, Ts datetime(4),meastype varchar(3),val float,units varchar(5), z float)")
          
        cur.execute("create table if not exists gap (Ts datetime(4), meastype char(5),val float )")

        conn.close()

   except mariadb.Error as e :
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)


# this function can create a database, and a table in the database. This database is not used, it was a test
def test():
	import sqlite3

	conn = sqlite3.connect('TestDB.db')  # You can create a new database by changing the name within the quotes
	cur = conn.cursor() # The database will be saved in the location where your 'py' file is saved

	# Create table - CLIENTS
	cur.execute('''CREATE TABLE CLIENTS
	             ([generated_id] INTEGER PRIMARY KEY,[Client_Name] text, [Country_ID] integer, [Date] date)''')
	conn.close()  


# Adds values in the measurements table
def add_measurements(cur, valhr, date, meastype, units):
   """Adds the given data to the measurements table"""  
  
   cur.execute("INSERT INTO measurements(Ts, meastype, val,units) VALUES (?, ?, ?,?)",
      (date, meastype,valhr, units))

# Add heart rate in the measurements table
def add_heartRate(cur, valhr, date):
   """Adds the given data to the measurements table"""
  
   cur.execute("INSERT INTO measurements(Ts, meastype, val,units) VALUES (?, ?, ?,?)",
      (date, 'HR',valhr, 'Bpm'))

# Add acceleration rate in the measurements table
def add_acc(cur, valacc, date,z):
   """Adds the given data to the mesurement table"""
  
   cur.execute("INSERT INTO measurements(Ts, meastype, val,units,z) VALUES (?, ?, ?,?,?)",
      (date, "Acc",valacc, "mg",z))


# Add energy in the measurements table
def add_energy(cur, val, date):
   """Adds the given data to the mesurement table"""
  
   cur.execute("INSERT INTO measurements(Ts, meastype, val,units) VALUES (?, ?, ?,?)",
      (date, "ene",val,"mg" ))



# Add value in the gap table
def add_gap(cur, meastype, val, date):
   """Adds the given data to the mesurement table"""
  
   cur.execute("INSERT INTO gap(Ts, meastype, val) VALUES (?, ?, ?)",
      (date, meastype ,val ))


# get the result of the query
def get_field_info(cur):
   """Retrieves the field info associated with a cursor"""

   field_info = mariadb.fieldinfo()

   field_info_text = []

   # Retrieve Column Information
   for column in cur.description:
      column_name = column[0]
      column_type = field_info.type(column)
      column_flags = field_info.flag(column)

      field_info_text.append(f"{column_name}: {column_type} {column_flags}")

   return field_info_text


# this function is called in the function gethr() of the file hr.py
def addhrtodb(valhr):
    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()

        #date and hour
        cur.execute("SELECT NOW(4);") # query for having the date and the time
        date = cur.fetchone() #get the first line of the result of the query,the format is a table
        date=date[0] #get the first element of the table 
        #add data
        add_heartRate(cur,valhr,date)
        #print table
        #get_tab(cur)    

        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# this function is called in the function getacc() of the file acc.py
def addacctodb(valacc,z):
# valacc : module of the acceleration rate ( valacc = sqrt(x2 + y2 + z2) ) 
# z = acceleration rate on the z axis
    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()

        #date and hour
        cur.execute("SELECT NOW(4);")  # query for having the date and the time
        date = cur.fetchone()  #get the first line of the result of the query,the format is a table
        date=date[0] #get the first element of the table 
        #add data        
        add_acc(cur,valacc,date,z)
        #print table
        #get_tab(cur)    

        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# for filling the table measurments with several acceleration rate values (nb is the number of values)
def addaccstodb(valacc,z,nb):
    try:
        conn=mariadb.connect(
                user = usernamme,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()

        #date and hour
        for x in range (0,nb) :
        	cur.execute("SELECT NOW(4);")
        	date = cur.fetchone()
        	date=date[0]
        	#add data        
        	add_acc(cur,valacc,date,z)

        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# adds a value in the table gap
def addgaptodb(meastype,val):
    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()

        #date and hour
        cur.execute("SELECT NOW(4);")
        date = cur.fetchone()
        date=date[0]
        #add data        
        add_gap(cur,meastype,val,date)
        #print table
        #get_tab(cur)    

        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# return 1 if the mean of the second group of values is bigger by "max" unit(s) than the mean of the 1st group of values
def moylast(meastype,nb1,nb2,delay, max,dim):
# meastype : heart rate or acceleration rate
# nb1 : the first number of values that we want to calculate the mean
# nb2 : the second number of values that we want to calculate the mean
# delay : the number of value betewen nb1 and nb2 
# max : the difference between the mean of nb1 and the mean of nb2 that we want to exceed 

    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()
        #delete val that refers to the polar  is no against the skin
        cur.execute(f"delete from measurements where val = 0 && meastype='HR'")
        
        #1 :calcul number of values
        cur.execute(f"select count(*) from measurements where meastype = '{meastype}' ;")
        total = cur.fetchone()
        total= total[0]
        # 2:if there are enough values, get the nb1 values
        if (total >= nb1+nb2+delay):
                firstvalue=total-nb1-nb2-delay
                cur.execute(f"select {dim} from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb1} ")
        elif (total > nb2+delay) : # to compare the mean of the last values between at least one value before the fall
                nb1= total-nb2-delay
                firstvalue= 0
                cur.execute(f"select {dim} from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb1} ")
        else:
        	nb1=total
        # 3: calcul moy of the 1st nb values
        moy1=0
        for data in cur.fetchall():
            moy1=moy1+data[0]
        moy1=moy1/nb1

        # get the last nb2 values
        firstvalue=total-nb2
        if firstvalue - delay <= 0:
                nb2 = total
                firstvalue = 0
        cur.execute(f"select {dim} from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb2} ")
        moy2 = 0
        for data in cur.fetchall():
            moy2=moy2+data[0]
        moy2=moy2/nb2
        diff = moy2-moy1

        conn.close()
 
        if diff >=max :
                print("diff average ",meastype,"  = " , diff,"   are you OK ?")
                return 1
        else : 
                print("diff average ",meastype," = " , diff,"  everything is OK")
                return 0

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# for retrieving values in the database
def getvalues(nb,meastype,time):
# nb : number of value that we want
# meastype : Acc or HR 
# time : where are the value in the database. 
# example : if we want the last 10 values of the heart rate 5 seconds ago : nb = 10, meastype = "HR", time = 5 ( because there is one value per second for the heart rate)
# example : if we want the last 10 values of the acceleration rate 5 seconds ago : nb = 10, meastype = "Acc", time = 5*50 (because there are 50 values per second for the acceleration rate)

    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()
        
        
        # get number of values in the database
        cur.execute(f"select count(*) from measurements where meastype = '{meastype}'  ")
        total = cur.fetchone()
        total= total[0]
        # go to the least recent value that we want
        firstvalue=total-nb-time
        # if there are not enough values in the database
        if firstvalue < 0:
                nb = total
                firstvalue = 0
        cur.execute(f"select val from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb} ")
        
        data=cur.fetchall()
        cur.execute(f"select Ts from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb} ")
        data=data+cur.fetchall()

        cur.execute(f"select z from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb} ")
        data=data+cur.fetchall()

        conn.close()

        return data
        
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)

# this function return 1 if the difference between the min and the max value of the nb values is bigger than "diff"       	
def accdiff(meastype,nb, diff,dim,time):
# meastype : accuracy rate or heart rate
# nb : number of value we want to analyse
# diff : the minimum difference that we expect between the min and the max value
# dim : dimension 
# time : number of values, when was the fall. exemple : if we want to know if there was a fall 20 sec ago, time = 20*50

	data=getvalues(nb,meastype,time)
	if dim=="val":
		accval = data[:nb-1]
	elif dim=="z":
		accval = data[-nb:]
		#print(accval)
	else:
		print("problem")
	if diff>(max(accval)[0]-min(accval)[0]) :
		return 0
	else :
		return 1

import statistics
# calculation of the energy and put the value in the database, this function can be called in the main file (thread2.py), 
# in function getmoy() for calculating the energy each second and to put the value in the database
def energie(meastype,nb):
# meastype : accuracy rate or heart rate
# nb : number of value we want to analyse
# diff : the minimum value of energy that we expect
    try:
        conn=mariadb.connect(
                user = username,
                password=userpassword,
                host="localhost",
                database=userdatabase)
        #Instantiate Cursor
        cur = conn.cursor()


        # get number of values in the database
        cur.execute(f"select count(*) from measurements where meastype = '{meastype}'  ")
        total = cur.fetchone()
        total= total[0]
        # go to the least recent value that we want
        firstvalue=total-nb
        # if there are not enough values in the database
        if firstvalue < 0:
                nb = total
                firstvalue = 0
        cur.execute(f"select val from measurements where meastype = '{meastype}' LIMIT {firstvalue},{nb} ")

        accval=cur.fetchall()

	# calculate the median 
        accval.sort()
        if len(accval)%2==0:
                med=((accval[(nb-1)//2][0]+accval[nb//2][0])/2)
        else :
                med=accval[nb//2][0]

	#calculate the energie with the substraction of the median
        energie =sum([(i[0]-med)*(i[0]-med) for i in accval ])
        cur.execute("SELECT NOW(4);")
        date = cur.fetchone()
        date=date[0]
        add_energy(cur, energie, date)
        conn.close()

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB : {e}")
        sys.exit(1)


# calculation of the energie and return 1 if the energy is lower than "diff" (that is sto say that we have a static position)
def accenergie(meastype,nb, diff):
# meastype : accuracy rate or heart rate
# nb : number of value we want to analyse
# diff : the minimum value of energy that we expect
        data=getvalues(nb,meastype,0)
        accval = data[:nb-1]
	
	# caluculate the median
        accval.sort()
        if len(accval)%2==0:
        	med=((accval[(nb-1)//2][0]+accval[nb//2][0])/2)
        else :
        	med=accval[nb//2][0]
        print("med:",med)
        energie =sum([(i[0]-med)*(i[0]-med) for i in accval ])
        print("energie:",energie)
        try:	
                conn=mariadb.connect(
                        user = username,
                        password=userpassword,
                        host="localhost",
                        database=userdatabase)
	        #Instantiate Cursor
                cur = conn.cursor()
                cur.execute("SELECT NOW(4);")
                date = cur.fetchone()
                date=date[0]
                add_gap(cur, "ene", energie, date)
        except mariadb.Error as e:
        	print(f"Error connecting to MariaDB : {e}")
        	sys.exit(1)
        diff = diff * (nb/50) / 25 #(because the value of diff is for the time after the fall = 25sec)	
        if (energie > diff):
        	return 0
        else :
        	return 1


