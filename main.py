from config import PORT
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import time
from dateutil.parser import parse

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


def nacitaj_udaje():
    url = 'http://dealan.sk/json3.php'
    response = requests.get(url)
    zdroje = response.json()
    localtime_int = time.time()
    for zdroj in zdroje:
        device_time = parse(zdroj['naposledy'])
        #print(localtime_int - device_time.timestamp())
        zdroj["time_diff"] = localtime_int - device_time.timestamp()
        # print(zdroj)
    return zdroje
# Routes:


@app.get("/")
async def root(request: Request):
    """
    Show dashboard of all sensors from 'http://dealan.sk/json3.php'
    """
    zdroje = nacitaj_udaje()
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "zdroje": zdroje, "time": localtime})


@app.get("/triedenie/{triedenie}", response_class=HTMLResponse)
async def sorted_root(request: Request, triedenie: str):
    """
    Show dashboard of all sensors (sorted) from 'http://dealan.sk/json3.php'
    """
    def myFunc(e):
        return e[triedenie]

    zdroje = nacitaj_udaje()
    zdroje.sort(key=myFunc)
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "triedenie": triedenie, "zdroje": zdroje, "time": localtime})


@app.get("/device/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """
    show information about one particural device (sensor)
    """
    url = 'http://dealan.sk/device.php?id='+id
    response = requests.get(url)
    zdroj = response.json()  # '{"id": 1}'  #
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("device.html", {"request": request, "id": id, "zdroj": zdroj, "time": localtime})


@app.get("/old")
async def old(request: Request):
    """
    show inline old php web
    """
    return templates.TemplateResponse("old.html", {"request": request})


# Code for running app
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0",
                port=int(PORT), reload=True, debug=True)
