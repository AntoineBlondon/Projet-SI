import time, os, json


PATH = "/home/pi/server/static/photos/img/servoconfig.txt"

exemple = {"active": 0, "manuel": 50, "automatique": "55:240:10"}

def is_fichier_cree():
    return os.path.exists(PATH)

def creer_fichier():
    with open(PATH, 'w') as file:
        file.close()


def get_configs():
    with open(PATH, 'r') as file:
        return file.readlines()

def get_config(cam):
    raw_config = get_configs()[cam]
    return txt2config(raw_config)


def txt2config(raw_config): #1|m:200|a:55,240:10
    config = {}
    config["active"] = int(raw_config.split('|')[0])
    config["manuel"] = int(raw_config.split('|')[1])
    config["automatique"] = raw_config.split('|')[2].strip()
    return config

def get_active_config(cam):
    return get_config(cam)["active"]

def config2txt(config):
    return f"{config['active']}|{config['manuel']}|{config['automatique']}"


def set_config(cam, config):
    Lines = []

    with open(PATH, 'r') as file:
        Lines = file.readlines()

    Lines[cam] = config2txt(config)

    with open(PATH, 'w') as file:
        file.writelines(Lines)

def toJson():
    list = []
    for cam in range(len(get_configs())):
        config = get_config(cam)
        config = json.dumps(config)
        list.append(config)
    return list