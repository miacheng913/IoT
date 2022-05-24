# fastapi
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends , Form
from fastapi import templating
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
#畫圖
import matplotlib.pyplot as plt

#mqtt
import paho.mqtt.client as mqtt
import numpy as np
# db
import dataset
import pymysql
pymysql.install_as_MySQLdb()

import models
import threading

import json
import time

#db



def draw(table_name) :
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    cmd = "select * from " + table_name + " ORDER BY time_stamp DESC limit 10"
    data_list = []
    time_list = []
    for row in db.query(cmd) :
        data_list.append(row['data'])
        time_list.append(row['time_stamp'])
    #print(time_list)
    x = np.array(time_list)  # 50x1 array between 0 and 2*pi
    y = np.array(data_list)                # cos(x)

    # plt.clf()
    # plt.grid(True)
    # plt.plot(x3, y3, 'r:')     # red dotted line (no marker)
    # plt.savefig('static/img/fig1.png')
    
    plt.clf()
    plt.grid(True)
    plt.plot(x, y, 'b-o') # blue solid line with filled circle marker
    plt.savefig('static/img/fig2.png')


        




test_str :str
 
#mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) )
    client.subscribe("/python/mqtt/hst")

def on_message(client, userdata, msg):
    global test_str
    
    print(msg.topic+" "+str(msg.payload))
    mqtt_str = msg.payload.decode('utf-8', errors='ignore') #bytes to str (中文目前無法處理)
    table= mqtt_str.split(':')
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    user_table = db[table[0]]

    insert_dic = {'data':table[1],'time_stamp':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    user_table.insert(insert_dic)
    #print(mqtt_str)
    #mqtt_j = json.loads(mqtt_str)  #str to JSON
    #print(mqtt_j)
    

def MQTT_server():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883)
    client.loop_forever()

# 建立一個子執行緒
t = threading.Thread(target = MQTT_server)

# 執行該子執行緒
t.start()





templates = Jinja2Templates(directory='templates')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


gdata : models.face_data

app.mount(path='/templates', app=StaticFiles(directory='templates'), name='templates')
app.mount(path='/static', app=StaticFiles(directory='static'), name='static ')

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    
    print(request)
    return templates.TemplateResponse(name='index.html', context={'request': request})

@app.get('/home', response_class=HTMLResponse)
async def index(request: Request):
    print(request)
    #draw('co2')
    return templates.TemplateResponse(name='home.html', context={'request': request})

@app.post('/record_face_data')
async def record_face_data(request: Request,data : models.face_data):
    print(data)
    global gdata 
    gdata = data

@app.get('/show')
async def index(request: Request):
    global gdata,test_str
    return templates.TemplateResponse(name='show.html', context={'request': request,'data':test_str})