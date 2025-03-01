import Var
import pymysql.cursors
from setuptools._distutils.log import debug
import discord
import traceback

host = Var.mysql_host
user = Var.mysql_user
password = Var.mysql_password
db = Var.mysql_db
port = Var.mysql_port
connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def get_connection():
    return connection

def init():
    create_guild_table()

def create_guild_table():
    connection = get_connection()
    # ギルドテーブル guild_table
    # guild_id: ギルドID
    # 