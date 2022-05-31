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

# db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
# cmd = "select * from " + table_name + " ORDER BY time_stamp DESC limit 10"
 
#mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) )
    client.subscribe("/python/mqtt/hst/+")

def on_message(client, userdata, msg):
    global test_str
    
    print(msg.topic+" "+str(msg.payload))
    msg_str = msg.payload.decode('utf-8', errors='ignore') #bytes to str (中文目前無法處理)
    table= msg.topic.split('/')
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    user_table = db[table[4]]

    insert_dic = {'data':msg_str,'time_stamp':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
    user_table.insert(insert_dic)
    #print(table)
    
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)

def MQTT_server():
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

@app.get('/show')
async def index(request: Request):
    global gdata,test_str
    return templates.TemplateResponse(name='show.html', context={'request': request,'data':test_str})

@app.get('/mqtt')
async def index(request: Request):
    client.publish("/python/mqtt/hst/cmd/light", "test")

@app.get('/newestdata')
async def index(request: Request):
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    result = {'co2': 0.0,'face':0,'light':650,'temperature':25}
    cmd = "select * from co2 ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        result['co2'] = tmp['data']
    cmd = "select * from face ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        result['face'] = tmp['data']
    cmd = "select * from light ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        result['light'] = tmp['data']
    cmd = "select * from dht22 ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        result['temperature'] = tmp['data']
    print(result)
    return json.dumps(result,ensure_ascii=False)