# fastapi
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends , Form
from fastapi import templating
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt

#mqtt
import paho.mqtt.client as mqtt
import numpy as np
# db
import dataset
import pymysql
import models


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
    
#mqtt
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc) )
    client.subscribe("MQTT")

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883)
client.loop_forever()



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
    global gdata
    return templates.TemplateResponse(name='show.html', context={'request': request,'data':gdata})