'''
    File: receiveCSV.py
    Author: Chase Carthen
    Description: The following file hosts a simple backend service for uploading data into a mysql.
'''
from datetime import datetime
from flask import Flask, request
#from werkzeug import secure_filename
from threading import Thread
from multiprocessing import Queue as queue
import signal 
import sys
from time import sleep
from csvprocessorsql import importCSVToMySQL,parseFileName
import os 
def handler(signal, frame):
  global running 
  running = False
  if not fileDataQueue.empty():
    sleep(60)
  sys.exit(0)
signal.signal(signal.SIGINT, handler)


app = Flask(__name__)

user=''
password=''
server='localhost:5000'

fileDataQueue = queue()
running = True
def processFiles():
    global user
    global password
    global server 
    while running:
        if not fileDataQueue.empty():
            data = fileDataQueue.get()
            importCSVToMySQL(csvstring=data['data'],datestart=data['startdate'], location=data['location'], userName=user, password=password, server=server)

@app.route("/csv", methods = ['POST'])
def upload_csv():

    location = request.args.get('location','Some Location')
    if request.method == 'POST':
        # handle post request
        f = request.files.get('files', None)
        if f != None:
            contents = f.read()
            contents = contents.decode()
            fileDataQueue.put({'data':contents, 'startdate':parseFileName(f.filename), "location":location})
            return 'file uploaded'
        else:
            if request.json:
                data = request.json
                if 'data' in data and 'startdate' in data:
                    fileDataQueue.put({'data':data['data'],'startdate':datetime.fromtimestamp(data['startdate']), "location":location})
                return 'data received'
            else:
                return 'Not Recieved',400

if __name__ == "__main__":
    running = True
    thread = Thread(target=processFiles)
    thread.start()
    '''
      user: cm9vdAo=
      password: SGFvUGFzc3dvcmQK
      service: haoinsertionservice.im.svc.cluster1.local
      dbheadofstring: mysql+pymysql
    '''
    if os.path.isdir('./config'):
        if os.path.isfile('./config/user'):
            user = open('./config/user','r').read()
        if os.path.isfile('./config/password'):
            password = open('./config/password','r').read()
        if os.path.isfile('./config/service'):
            server = open('./config/service','r').read()
        print(user)
        print(password)
        print(server)
    app.run(host='0.0.0.0')
    running = False
    thread.join()
