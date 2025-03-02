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
    # guild_id: サポートギルドID
    # linked_guild_id: 紐づけギルドID
    with connection.cursor() as cursor:
        sql = "CREATE TABLE IF NOT EXISTS guild_ticket (id INT PRIMARY KEY AUTO_INCREMENT, guild_id VARCHAR(255), linked_guild_id VARCHAR(255))"
        cursor.execute(sql)

def get_guild_id_list(linked_guild_id) -> list:
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT guild_id FROM guild_ticket WHERE linked_guild_id = %s"
        cursor.execute(sql, (linked_guild_id))
        result = cursor.fetchall()
        guild_id_list = []
        for row in result:
            guild_id_list.append(row['guild_id'])
        return guild_id_list