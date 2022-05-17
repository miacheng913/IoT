# fastapi
from fastapi import FastAPI, Request, Response, HTTPException, status, Depends , Form
from fastapi import templating
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import matplotlib.pyplot as plt
import numpy as np
# db
import dataset
import pymysql

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
    


templates = Jinja2Templates(directory='templates')


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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