#=====================================
# Author        : Sandesh Sonawane
# Date          : 25 May 2020
# Project Name  : API Communication
#===================================== 
import os
import sys
from flask import Flask
from flask_mysqldb import MySQL
import re
import json
from datetime import datetime, timedelta
from flask_cors import CORS
from flask import request
from flask import jsonify

app = Flask(__name__)
#CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})

#logging.getLogger('flask_cors').level = logging.DEBUG

app.config['MYSQL_HOST'] = '127.0.0.1'#'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'yourdbpassword'
app.config['MYSQL_DB'] = 'yourdbname'#'parking'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


#--------------------- Timestamp -------------------------------
def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
#--------------------- Timestamp -------------------------------

@app.route("/")
def helloWorld():
  return "Hello, This is Neha"

@app.route('/machinedata', methods=['GET'])
def machinedata():
    print "************ Day Machine Data ************************"
    global currentDate
    print currentDate
    cur = mysql.connection.cursor()
    cur.execute("select DATE_FORMAT(startTime, '%H:%i:%s') AS 'startTime',DATE_FORMAT(endTime, '%H:%i:%s') AS 'endTime', DATE_FORMAT(totalTime, '%H:%i:%s') AS 'totalTime',  driveName from data where startDate = '2020-05-25")
    results = cur.fetchall()
    print "============= results ========================="
    print results
    print "======================================="
    dataList = {}
    for e in results:
        #print e
        #print e.get('driveName')
        #dataList[e.get('startTime')] = str(e.get('driveName'))
        results1 = json.dumps(results)

    results2 = {
        "status":"OK",
        "code":200,
        "message":"Data fetch successfully",
        "data" : results1,
        }


    return (results1)
  
  
@app.route('/sandesh', methods=['POST'])
def sandesh():
   if request.method=='POST':
         print request.json
		 action = request.json['action']
		 print action
    	 message = "Request received successfully",
#--------------------------------- Action Start -------------------------------------------
   if action == "stadium":
	print "----------------------------------------------------------------------------"
	print "Stadium Lights ON"
	print "----------------------------------------------------------------------------"


   elif action == "ambulance":
	print "----------------------------------------------------------------------------"
	print "Stadium Green Light ON"
	print "----------------------------------------------------------------------------"

   else:
	print "----------------------------------------------------------------------------"
	return jsonify({'data':message})
#--------------------------------- Action End ---------------------------------------------
if __name__ == '__main__':
 app.run(host='0.0.0.0')
