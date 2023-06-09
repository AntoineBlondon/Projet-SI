"""
Import des fonctions
os : pour lire/écrire dans les fichiers
config : notre fichier pour piloter le moteur
flask : qui permet le fonctionnement de la page web
"""
import os
from config import *
from flask import Flask, render_template, redirect, request

# Défini app comme étant un objet de Flask, ici la page web
app = Flask(__name__)

# Défini que la fonction en-dessous sera lancée lors d'une connexion à la page web à "/" (=racine =première page ouverte)
@app.route("/", methods=['POST', 'GET'])
def index():
    """
    Envoie certaines infomations dans la page web (comme les caméras utilisées, les photos ou les configurations)
    """
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
    """
    Modifie le fichier de configuration avec les paramètres associés si l'on applique le mode manuel au moteur
    """
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
    """
    Modifie le fichier de configuration avec les paramètres associés si l'on applique le mode automatique au moteur
    """
    if request.method == 'GET':
        info = request.args.get('info')
        cam = int(request.args.get('cam'))
        config=get_config(cam)
        config["active"]=1
        config["automatique"] = info
        set_config(cam,config)
    return redirect("/?cam=" + str(cam))



def getFiles():
    """
    Récupère l'emplacement de toutes les images des caméras
    """
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
