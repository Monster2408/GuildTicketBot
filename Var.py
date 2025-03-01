import discord
# import pya3rt
from datetime import datetime
import yaml

BOT_VERSION = "1.0.0"
BOT_MODULE = "discord.py"

DEBUGMODE = False

# EXPの係数
EXP_COEFFICIENT: float = 107.95

# YAML 設定ファイルを読み込む関数
def load_config(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config("config.yml")
if DEBUGMODE:
    config = load_config("config_debug.yml")

try:
    token = config["token"]
    mysql_host = config["database"]["host"]
    mysql_user = config["database"]["user"]
    mysql_password = config["database"]["password"]
    mysql_db = config["database"]["database"]
    mysql_port = config["database"]["port"]
except Exception:
    token = ""
    mysql_host = ""
    mysql_user = ""
    mysql_password = ""
    mysql_db = ""
    mysql_port = ""
    
