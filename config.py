"""
import des modules utilisés
time : pour les temps d'attente
wiringpi : pour commander le moteur
os : pour accéder au fichier de configuration
"""
import time, os, json

# Définition du chemin vers le fichier de configuration
PATH = "/home/pi/server/static/photos/img/servoconfig.txt"

exemple = {"active": 0, "manuel": 50, "automatique": "55:240:10"}

def is_fichier_cree():
    """
    Vérifie si le fichier de configuration existe
    """
    return os.path.exists(PATH)

def creer_fichier():
    """
    Crée le fichier de configuration
    """
    with open(PATH, 'w') as file:
        file.close()


def get_configs():
    """
    Récupère toutes les lignes du fichier de configuration (= toutes les configurations)
    """
    with open(PATH, 'r') as file:
        return file.readlines()

def get_config(cam):
    """
    Récupère la configuration de la cam "cam"
    """
    raw_config = get_configs()[cam]
    return txt2config(raw_config)


def txt2config(raw_config): #1|m:200|a:55,240:10
    """
    Renvoie la configuration sous forme d'un dictionnaire (pour faciliter l'exploitation des données par Python)
    """
    config = {}
    config["active"] = int(raw_config.split('|')[0])
    config["manuel"] = int(raw_config.split('|')[1])
    config["automatique"] = raw_config.split('|')[2].strip()
    return config

def get_active_config(cam):
    """
    Récupère le configuration active de "cam"
    """
    return get_config(cam)["active"]

def config2txt(config):
    """
    Renvoie la configuration sous forme d'un string (texte) pour l'écriture dans le fichier de configuration
    """
    return f"{config['active']}|{config['manuel']}|{config['automatique']}"


def set_config(cam, config):
    """
    Modifie la configuration "cam" dans le fichier de configuration
    """
    Lines = []

    with open(PATH, 'r') as file:
        Lines = file.readlines()

    Lines[cam] = config2txt(config)

    with open(PATH, 'w') as file:
        file.writelines(Lines)

def toJson():
    """
    Transforme le disctionaire des configurations au format JSON pour qu'il soit utilisable et lisble en JavaScript pour le serveur web
    """
    list = []
    for cam in range(len(get_configs())):
        config = get_config(cam)
        config = json.dumps(config)
        list.append(config)
    return list
