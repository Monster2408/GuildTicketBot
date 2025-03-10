import Var
import pymysql.cursors

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
    create_guild_member_table()
    create_delete_guild_table()

def create_guild_table():
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS guild_ticket (
            id INT PRIMARY KEY AUTO_INCREMENT,
            guild_id VARCHAR(255) UNIQUE,
            linked_guild_id VARCHAR(255)
        )
        """
        cursor.execute(sql)
    connection.commit()

def create_guild_member_table():
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS guild_member (
            id INT PRIMARY KEY AUTO_INCREMENT,
            member_id VARCHAR(255),
            guild_id VARCHAR(255),
            linked_guild_id VARCHAR(255),
            invite_url TEXT,
            UNIQUE (member_id, guild_id)
        )
        """
        cursor.execute(sql)
    connection.commit()

def create_delete_guild_table():
    # guild_idとtimeを持つテーブルを作成(timeは分単位)
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """
        CREATE TABLE IF NOT EXISTS delete_guild (
            id INT PRIMARY KEY AUTO_INCREMENT,
            guild_id VARCHAR(255) UNIQUE,
            time INT
        )
        """
        cursor.execute(sql)
    connection.commit()

def get_guild_id_list(linked_guild_id) -> list:
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT guild_id FROM guild_ticket WHERE linked_guild_id = %s"
        cursor.execute(sql, (linked_guild_id,))
        result = cursor.fetchall()
        return [row['guild_id'] for row in result]

def link_guild(guild_id, linked_guild_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO guild_ticket (guild_id, linked_guild_id)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE linked_guild_id = VALUES(linked_guild_id)
        """
        cursor.execute(sql, (guild_id, linked_guild_id))
    connection.commit()

def get_support_guild_id_list() -> list:
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT guild_id FROM guild_ticket"
        cursor.execute(sql)
        result = cursor.fetchall()
        return [row['guild_id'] for row in result]

def get_member_guild(member_id: int, linked_guild_id: int) -> str:
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT guild_id FROM guild_member WHERE member_id = %s AND linked_guild_id = %s"
        cursor.execute(sql, (member_id, linked_guild_id))
        result = cursor.fetchone()
        if result is None:
            return None
        return result['guild_id']

def get_invite_url(member_id, guild_id):
    """ 指定された member_id と guild_id に紐づいた招待リンクを取得する """
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT invite_url FROM guild_member WHERE member_id = %s AND guild_id = %s"
        cursor.execute(sql, (member_id, guild_id))
        result = cursor.fetchone()
        return result["invite_url"] if result and result["invite_url"] else None

def update_invite_url(member_id, guild_id, linked_guild_id, invite_url):
    """ 指定された member_id と guild_id に紐づいた招待リンクを更新 or 挿入 """
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = """
        INSERT INTO guild_member (member_id, guild_id, linked_guild_id, invite_url)
        VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE invite_url = VALUES(invite_url)
        """
        cursor.execute(sql, (member_id, guild_id, linked_guild_id, invite_url))
    connection.commit()

def get_delete_time(guild_id):
    connection = get_connection()
    with connection.cursor() as cursor:
        sql = "SELECT time FROM delete_guild WHERE guild_id = %s"
        cursor.execute(sql, (guild_id,))
        result = cursor.fetchone()
        return result["time"] if result and result["time"] else -1

def set_delete_time(guild_id, time):
    connection = get_connection()
    if time == -999:
        # テーブルから削除
        with connection.cursor() as cursor:
            sql = "DELETE FROM delete_guild WHERE guild_id = %s"
            cursor.execute(sql, (guild_id,))
    else:
        with connection.cursor() as cursor:
            sql = """
            INSERT INTO delete_guild (guild_id, time)
            VALUES (%s, %s)
            ON DUPLICATE KEY UPDATE time = VALUES(time)
            """
            cursor.execute(sql, (guild_id, time))
    connection.commit()