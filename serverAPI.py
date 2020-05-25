#=====================================
# Author        : Sandesh Sonawane
# Date          : 13 May 2020
# Project Name  : API Communication
#===================================== 

from flask import Flask
from flask_mysqldb import MySQL
import re
import json
from datetime import datetime, timedelta
from flask_cors import CORS
from flask import request


app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

#logging.getLogger('flask_cors').level = logging.DEBUG

app.config['MYSQL_HOST'] = '127.0.0.1'#'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'teamlabs@123'
app.config['MYSQL_DB'] = 'teamlabs'#'parking'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


#==========================================================================================

IDEAL_CYCLE_TIME_SECS = 3600                # 1 hour = 60 min = 3600 secs
PLAN_PRODUCTION_SECS = 3600*9               # Shift duration in hours = 9 hour = 9*3600 secs
PLAN_PRODUCTION_QUANTITY_PER_DAY = 10       # Planned production quantity per day
PLAN_PRODUCTION_QUANTITY_PER_WEEK = 60       # Planned production quantity per week
PLAN_PRODUCTION_QUANTITY_PER_MONTH = 300    # Planned production quantity per month
SHIFT_END_TIME = 3600*18                    # Shift end time = 18 (6 PM) * 3600 = 18*3600 secs

#==========================================================================================

#====================================================================================================
oee = None
performance = None
quality = None
currentDate = None

ydoee = None
ydperformance = None
ydquality = None

wkoee = None
wkperformance = None
wkquality = None

mtoee = None
mtperformance = None
mtquality = None


now = datetime.now()
print "========= Today datetime ==========================="
print now
print "========= Today date ==============================="
currentDate = now.strftime("%Y-%m-%d")
print currentDate
print "========= Current time ============================="
current_time = now.strftime("%H:%M:%S")
#print("Current Time =", current_time)
currentTime = (current_time)
print currentTime
#===================== API Route Start ==============================================================
@app.route("/")
def helloWorld():
  return "Hello, This is Neha"

@app.route('/machinedata', methods=['GET'])
def machinedata():
    print "************ Day Machine Data ************************"
    global currentDate
    print currentDate
    cur = mysql.connection.cursor()
    #cur.execute('''select * from raw_parameter order by id desc limit 1''')
    #cur.execute('''select DATE_FORMAT(timestamp, '%d-%m %H:%i:00') AS 'timestamp' , parameter_value, unit from raw_parameter where machine_name = 'CBR' and parameter_name = 'TEMPERATURE' group by FROM_UNIXTIME(FLOOR((UNIX_TIMESTAMP(timestamp))/60)*60)''')
    #cur.execute('''select DATE_FORMAT(totalTime, '%d-%m %H:%i:00') AS 'totalTime' , driveName from data group by FROM_UNIXTIME(FLOOR((UNIX_TIMESTAMP(totalTime))/60)*60) order by id desc limit 1''')
    #cur.execute('''select DATE_FORMAT(totalTime, '%d-%m %H:%i:00') AS 'totalTime' , driveName from data group by FROM_UNIXTIME(FLOOR((UNIX_TIMESTAMP(totalTime))/60)*60) order by id desc limit 1''')
    cur.execute("select DATE_FORMAT(startTime, '%H:%i:%s') AS 'startTime',DATE_FORMAT(endTime, '%H:%i:%s') AS 'endTime', DATE_FORMAT(totalTime, '%H:%i:%s') AS 'totalTime',  driveName from data where startDate = '"+ currentDate +"'")
    results = cur.fetchall()
    #print results[0]
    #results1 = json.dumps(results[0])
    print "============= results ========================="
    print results
    print "======================================="
    dataList = {}
    for e in results:
        #print e
        #print e.get('driveName')
        #dataList[e.get('startTime')] = str(e.get('driveName'))
        results1 = json.dumps(results)

        #dataList1 = json.dumps(dataList)

    #print "==================== Result1 ==================="
    #print results1
    #print "==================== dataList1 ================"
    #print dataList1


    results2 = {
        "status":"OK",
        "code":200,
        "message":"Data fetch successfully",
        "data" : results1,
        }


    return (results1)

@app.route('/usecase', methods=['POST']) #(192.168.1.209:5000/usecase)
def usecase_scan():
   if request.method=='POST':
         print request.json
#--------------------------------- Print seperate data Start ------------------------------
         x =  json.dumps(request.json)
         y = json.loads(x)
         print (y["action"])
         task = (y["action"])

#--------------------------------- Action Start -------------------------------------------
   if task == "usecase1":
      print "One"
      response = 'One'
      #ser.write("1")
      return json.dumps(response)

   if task == "usecase2":
      print "Two"
      response = 'Two'
      #ser.write("2")
      return json.dumps(response)

   return json.dumps(response)

#===== This section is used for Enter stoppage reason from frontend and insert/update data in backend =====
@app.route('/poststoppages', methods=['POST']) #(192.168.1.209:5000/usecase)
def poststoppages():
   if request.method=='POST':
         #print request.json
        x =  json.dumps(request.json)
        print x
        y = json.loads(x)
        #print y
        comment     = (y["comment"])
        print comment

        if comment == "start":
            clientName  = (y["clientName"])
            location    = (y["location"])
            machine     = (y["machine"])
            reason      = (y["reason"])
            start_time  = (y["start_time"])
            remark      = (y["remark"])

            #========== Print Data ============
            print comment
            print clientName
            print location
            print machine
            print reason
            print start_time
            print remark
            #==================================
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO stoppageReason (clientName, location, machine, reason, start_time, remark) VALUES \
                        (%s, %s, %s, %s, %s, %s)", (clientName, location, machine, reason, start_time, remark))
            mysql.connection.commit()
            count = cur.rowcount
            print count            
            cur.close()
            response = 'Insert Recieved'
            return json.dumps(response)

        if comment == "end":
            clientName  = (y["clientName"])
            location    = (y["location"])
            machine     = (y["machine"])
            reason      = (y["reason"])
            end_time    = (y["end_time"])
            remark      = (y["remark"])

            #========== Print Data ============
            print comment
            print clientName
            print location
            print machine
            print reason
            print end_time
            print remark
            #==================================
            cur = mysql.connection.cursor()
            cur.execute("UPDATE stoppageReason set end_time = '"+end_time+"' where clientName = '"+clientName+"' and location = '"+location+"' and  machine = '"+machine+"' and reason = '"+reason+"' and end_time is NULL order by id asc limit 1")
            mysql.connection.commit()
            #print(cur.rowcount, "record(s) affected")
            count = cur.rowcount
            print count
            cur.close()
            if count == 0:
                response = 'No rows affected'
                return json.dumps(response)
            else:
                response = 'Update Recieved'
                return json.dumps(response)                         

        cur = mysql.connection.cursor()
        return json.dumps(response)

#===== This section is used for get all stoppages details from backend ================
@app.route('/getstoppages', methods=['POST'])
def getstoppages():

    if request.method=='POST':
        x =  json.dumps(request.json)
        print x
        y = json.loads(x)
        clientName  = (y["clientName"])
        location    = (y["location"])
        machine     = (y["machine"])
        dateTime      = (y["dateTime"])
       
        print clientName
        print location
        print machine
        print dateTime
        
        cur = mysql.connection.cursor()
        cur.execute("select id, clientName, location, machine, reason, DATE_FORMAT(start_time, '%Y-%m-%d %H:%i:%s') AS 'start_time', DATE_FORMAT(end_time, '%Y-%m-%d %H:%i:%s') AS 'end_time', CONVERT(((UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time))/60), CHAR) AS totalStoppageTime, remark from stoppageReason where clientName = '"+clientName+"' and location = '"+location+"' and machine = '"+machine+"' and start_time like '"+dateTime+"%'")
        results = cur.fetchall()
        results1 = json.dumps(results)
        count = cur.rowcount
        print "Total Rows : "+str(count)
        response="data received"
        return json.dumps(results)

#===== This section is used for login credentials (Enter username and password from frontend, and validate 
# with backend) ============
@app.route('/login', methods=['POST']) #(192.168.1.209:5000/usecase)
def login():
   if request.method=='POST':
        x =  json.dumps(request.json)
        print x
        y = json.loads(x)

        username  = (y["username"])
        password  = (y["password"])

        print username
        print password

        cur = mysql.connection.cursor()
        cur.execute("select username, password from login where username = '"+username+"' and password = '"+password+"'")
        mysql.connection.commit()
        #print(cur.rowcount, "record(s) affected")
        count = cur.rowcount
        print count            
        cur.close()

        if count == 0:
            #response = 'Incorrect'
            results = {
                "status":"OK",
                "code":200,
                "message":"Incorrect",
                "owner":"NA",
            }
            return json.dumps(results)
        else:
            cur = mysql.connection.cursor()
            cur.execute("select username, password, owner, clientName, location from login where username = '"+username+"' and password = '"+password+"' and active = 1")
            results = cur.fetchall()
            print results
            for e in results:
                owner      = e.get('owner')
                clientName = e.get('clientName')
                location   = e.get('location')
                #print owner
            mysql.connection.commit()
            #print(cur.rowcount, "record(s) affected")
            count = cur.rowcount
            print count            
            cur.close()

            if count == 0:
                #response = 'Inactive'
                results = {
                    "status":"OK",
                    "code":200,
                    "message":"Inactive",
                    "owner":"NA"
                }
                return json.dumps(results)                 

            else:
                #response = 'Correct'
                results = {
                    "status":"OK",
                    "code":200,
                    "message":"Correct",
                    "clientName":clientName,
                    "location":location,
                    "owner":owner
                }

                return json.dumps(results)                         

#===================== API Route End ==============================================================


if __name__ == '__main__':
    app.run(host='0.0.0.0')
