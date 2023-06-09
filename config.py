"""
import des modules utilisés
time : pour les temps d'attente
wiringpi : pour commander le moteur
os : pour accéder au fichier de configuration
"""
import time, wiringpi, os

# Définition de la caméra de cette carte
CAM = 0
# Définition du chemin vers le fichier de configuration
PATH = "../../partage/img/servoconfig.txt"

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
    config["automatique"] = raw_config.split('|')[2]
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


def add_config(config):
    """
    Ajoute une configuration au fichier de configuration
    """
    with open(PATH, 'a') as file:
        file.write(config2txt(config))

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

def setup():
    """
    Exécute les fonctions d'initialisation pour pouvoir piloter le moteur
    """
    wiringpi.wiringPiSetupGpio()

    wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
    wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

    wiringpi.pwmSetClock(192)
    wiringpi.pwmSetRange(2000)

def move(angle):
    """
    Fait bouger le moteur pour le mettre à l'angle "angle"
    """
    # 142,5 = milieu
    try:
        wiringpi.pwmWrite(18, angle)
    except:
        wiringpi.pwmWrite(18, 55)


def go():
    """
    Fonction principale qui lit le fichier de configuration et pilote la caméra en fonction de celui-ci
    """
    setup()
    angle=0
    while True:
        config = get_config(0)
        if config["active"] == 0:
            angle=int(config["manuel"]*0.97+50)
            
            move(angle)
        else:
            config["start"] = int(config["automatique"].split(':')[0])
            config["stop"] = int(config["automatique"].split(':')[1])
            config["time"] = int(config["automatique"].split(':')[2])

            delay_period = float(config["time"]) / float(abs(config["stop"] - config["start"]))
            for pulse in range(config["start"], config["stop"], 1):
                angle=pulse
                wiringpi.pwmWrite(18, angle)
                time.sleep(delay_period)
            for pulse in range(config["stop"], config["start"], -1):
                angle=pulse
                wiringpi.pwmWrite(18, angle)
                time.sleep(delay_period)
        time.sleep(1)








def main():
    """
    Exécute la fonction principale au lancement du fichier
    """
    if not is_fichier_cree():
        creer_fichier()
    
    #add_config({"active": 1, "mode": 'm', "consigne": 140})
    #add_config({"active": 0, "mode": 'a', "start": 140, "stop": 200, "time": 10})

    go()



main()