import os
from dotenv import dotenv_values
import mysql.connector

ENV = {**dotenv_values(".env.local"), **os.environ}

MYSQL_HOST = ENV.get("MYSQL_HOST", "127.0.0.1")
MYSQL_PORT = int(ENV.get("MYSQL_PORT", "3306"))
MYSQL_USER = ENV.get("MYSQL_USER", "root")
MYSQL_PASSWORD = ENV.get("MYSQL_ROOT_PASSWORD", "root_pwd")
MYSQL_DB = ENV.get("MYSQL_DATABASE", "pizza_mysql")


def get_mysql_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        connection_timeout=3
    )
