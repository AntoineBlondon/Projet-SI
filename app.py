import os
from config import *
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def index():
    cam = 0
    try:
        if request.method == 'GET':
            cam = int(request.args.get('cam'))
    except:
        pass
    photos=getFiles()
    configurations = toJson()
    return render_template("page.html",photos=photos,configs=configurations,len=len(configurations),cam=cam)


@app.route("/manuel", methods=['POST', 'GET'])
def manuel():
    if request.method == 'GET':
        amount = int(request.args.get('amount'))
        cam = int(request.args.get('cam'))
        config=get_config(cam)
        config["active"]=0
        config["manuel"] = amount
        set_config(cam,config)
    return redirect("/?cam=" + str(cam))

@app.route("/automatique", methods=['POST', 'GET'])
def automatique():
    if request.method == 'GET':
        info = request.args.get('info')
        cam = int(request.args.get('cam'))
        config=get_config(cam)
        config["active"]=1
        config["automatique"] = info
        set_config(cam,config)
    return redirect("/?cam=" + str(cam))



def getFiles():
    distant_pictures = os.listdir("/home/pi/server/static/photos/img")
    local_pictures = os.listdir("/home/pi/server/static")
    files_list = []
    for i in range(len(distant_pictures)):
        files_list.append("../static/photos/img/" + distant_pictures[i])
    
    for i in range(len(local_pictures)):
        files_list.append("../static/" + local_pictures[i])
    
    sorted_list = []
    for i in files_list:
        if i.endswith(".jpg"):
            sorted_list.append(i)
    return sorted_list