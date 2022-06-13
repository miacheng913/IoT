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
from datetime import datetime
import pymysql
pymysql.install_as_MySQLdb()

import models
import threading

import json
import time

#db

# db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
# cmd = "select * from " + table_name + " ORDER BY time_stamp DESC limit 10"
 
state = "alto"

state_table = {"dht22":["23", "fan", "0" ,"1" ,"fan"],"light":["650" ,"light" ,"101" ,"100", "light1"],"face":["1", "monitor", "0" ,"1", "monitor"],"co2":["500" ,"light" ,"111", "110" ,"light2"]}
state_now_table = {"fan":"0","light1":"0","monitor":"0","light2":"0"}

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
    if user_table != "cmd" :
        insert_dic = {'data':msg_str,'time_stamp':time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}
        user_table.insert(insert_dic)
    else :
        print("I publish")
    #print(table)
    global state,state_table
    if state == "alto":
        if float(msg_str) < float(state_table[table[4]][0]):
            MQTT_send("/python/mqtt/hst/cmd/"+state_table[table[4]][1],state_table[table[4]][2])
            state_now_table[state_table[table[4]][4]] = state_table[table[4]][2]
            print(state_now_table)
        else:
            MQTT_send("/python/mqtt/hst/cmd/"+state_table[table[4]][1],state_table[table[4]][3])
            state_now_table[state_table[table[4]][4]] = state_table[table[4]][3]
            print(state_now_table)
    

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.emqx.io", 1883)

def MQTT_server():
    client.loop_forever()

# 建立一個子執行緒
t = threading.Thread(target = MQTT_server)

# 執行該子執行緒
t.start()

def MQTT_send(topic,data):
    client.publish(topic, data)

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

def newest():
    global state,state_table,state_now_table
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    
    cmd = "select * from co2 ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        if float(tmp['data']) < float(state_table['co2'][0]):
            state_now_table['light2'] = state_table['co2'][2]
        else:
            state_now_table['light2'] = state_table['co2'][3]
    cmd = "select * from face ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        if float(tmp['data']) < float(state_table['face'][0]):
            state_now_table['monitor'] = state_table['face'][2]
        else:
            state_now_table['monitor'] = state_table['face'][3]
    cmd = "select * from light ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        if float(tmp['data']) < float(state_table['light'][0]):
            state_now_table['light1'] = state_table['light'][2]
        else:
            state_now_table['light1'] = state_table['light'][3]
    cmd = "select * from dht22 ORDER BY time_stamp DESC limit 1"
    for tmp in db.query(cmd):
        if float(tmp['data']) < float(state_table['dht22'][0]):
            state_now_table['fan'] = state_table['dht22'][2]
        else:
            state_now_table['fan'] = state_table['dht22'][3]
    
    print(state_now_table)



@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    
    print(request)
    return templates.TemplateResponse(name='index.html', context={'request': request})

@app.get('/home', response_class=HTMLResponse)
async def index(request: Request):
    print(request)
    #draw('co2')
    return templates.TemplateResponse(name='home.html', context={'request': request})

@app.get('/control')
async def index(request: Request):
    newest()
    return templates.TemplateResponse(name='control.html', context={'request': request})

@app.get('/history')
async def index(request: Request):
    return templates.TemplateResponse(name='history.html', context={'request': request})

@app.get('/mqtt')
async def index(request: Request):
    client.publish("/python/mqtt/hst/cmd/light", "test")

@app.get('/state')
async def index(request: Request):
    global state_now_table
    #print(result)
    return json.dumps(state_now_table,ensure_ascii=False)

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
    #print(result)
    return json.dumps(result,ensure_ascii=False)

@app.get('/historydata')
async def index(request: Request):
    db = dataset.connect('mysql://IOT:Sea13Sky17@127.0.0.1:3306/iot?charset=utf8mb4')
    result = {'co2': [],'face':[],'light':[],'temperature':[],'time_stamp':[]}
    cmd = "select * from co2 ORDER BY time_stamp DESC limit 20"
    for tmp in db.query(cmd):
        result['co2'].append(tmp['data'])
        result['time_stamp'].append(datetime.strftime(tmp['time_stamp'], "%Y-%m-%d %H:%M:%S"))
    cmd = "select * from face ORDER BY time_stamp DESC limit 20"
    for tmp in db.query(cmd):
        result['face'].append(tmp['data'])
    cmd = "select * from light ORDER BY time_stamp DESC limit 20"
    for tmp in db.query(cmd):
        result['light'].append(tmp['data'])
    cmd = "select * from dht22 ORDER BY time_stamp DESC limit 20"
    for tmp in db.query(cmd):
        result['temperature'].append(tmp['data'])
    #print(result)
    result['co2'] = list(reversed( result['co2']))
    result['time_stamp'] = list(reversed( result['time_stamp']))
    result['face'] = list(reversed( result['face']))
    result['light'] = list(reversed( result['light']))
    result['temperature'] = list(reversed( result['temperature']))
    return json.dumps(result,ensure_ascii=False)

@app.post("/cmd/{cmd}")
async def read_item(cmd ):
    print(cmd)
    tmp= cmd.split(':')
    MQTT_send("/python/mqtt/hst/cmd/"+tmp[0],tmp[1])

@app.post("/state/{state_now}")
async def read_item(state_now):
    global state
    state = str(state_now)
    print(state)