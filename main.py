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
import models
import threading

import json


def draw() :
    x = np.linspace(0.0, 2*np.pi)  # 50x1 array between 0 and 2*pi
    y = np.cos(x)                  # cos(x)

    x3 = np.linspace(0, 2*np.pi,10) # 10x1 array
    y3 = np.sinc(x3)

    plt.clf()
    plt.grid(True)
    plt.plot(x3, y3, 'r:')     # red dotted line (no marker)
    plt.savefig('static/img/fig1.png')
    
    plt.clf()
    plt.grid(True)
    plt.plot(x, y, 'b-o') # blue solid line with filled circle marker
    plt.savefig('static/img/fig2.png')


test_str :str
 
#mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) )
    client.subscribe("MQTT")

def on_message(client, userdata, msg):
    global test_str
    
    print(msg.topic+" "+str(msg.payload))
    mqtt_str = msg.payload.decode('utf-8', errors='ignore') #bytes to str (中文目前無法處理)
    #print(mqtt_str)
    mqtt_j = json.loads(mqtt_str)  #str to JSON
    print(mqtt_j)
    

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

def json_into_database(json):
    type = json['type']
    data = json["data"]
    time_stemp =  json["time"]

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
    draw()
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