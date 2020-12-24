from config import PORT
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import requests
import time

url = 'http://dealan.sk/json3.php'

app = FastAPI()

app.mount("/static", StaticFiles(directory="./static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get("/")
async def root(request: Request):
    """
    Show dashboard of all sensors from 'http://dealan.sk/json3.php'
    """
    response = requests.get(url)
    zdroje = response.json()
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "zdroje": zdroje, "time": localtime})


@app.get("/{triedenie}", response_class=HTMLResponse)
async def sorted_root(request: Request, triedenie: str):
    """
    Show dashboard of all sensors (sorted) from 'http://dealan.sk/json3.php'
    """
    def myFunc(e):
        return e[triedenie]
    response = requests.get(url)
    zdroje = response.json()
    #print("Triedenie:", triedenie, "je typu:", type(triedenie))
    zdroje.sort(key=myFunc)
    localtime = time.asctime(time.localtime(time.time()))
    return templates.TemplateResponse("home.html", {"request": request, "triedenie": triedenie, "zdroje": zdroje, "time": localtime})


@app.get("/device/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    """
    show information about one particulal device (sensor)
    """
    return templates.TemplateResponse("device.html", {"request": request, "id": id})

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(
        PORT), reload=True, debug=True)
