from config import PORT
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import time


app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")

# Routes


@app.get("/")
async def root(request: Request):
    """
    Show dashboard of all sensors from 'http://dealan.sk/json3.php'
    """
    url = 'http://dealan.sk/json3.php'
    response = requests.get(url)
    zdroje = response.json()
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "zdroje": zdroje, "time": localtime})


@app.get("/triedenie/{triedenie}", response_class=HTMLResponse)
async def sorted_root(request: Request, triedenie: str):
    """
    Show dashboard of all sensors (sorted) from 'http://dealan.sk/json3.php'
    """
    def myFunc(e):
        return e[triedenie]
    url = 'http://dealan.sk/json3.php'
    response = requests.get(url)
    zdroje = response.json()
    # zdrojes = sorted(zdroje)
    # print(zdrojes)
    # print("zdroje[0]['id']:", zdroje[0]['id'],
    #       "je typu:", type(zdroje[0]['id']))
    zdroje.sort(key=myFunc)
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "triedenie": triedenie, "zdroje": zdroje, "time": localtime})


@app.get("/device/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """
    show information about one particulal device (sensor)
    """
    url = 'http://dealan.sk/device.php'
    response = requests.get(url)
    zdroje = response.json()
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("device.html", {"request": request, "id": id, "zdroje": zdroje, "time": localtime})


@app.get("/old")
async def old(request: Request):
    """
    show inline old php web
    """
    return templates.TemplateResponse("old.html", {"request": request})

# code for running easily
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(PORT), reload=True, debug=True)
