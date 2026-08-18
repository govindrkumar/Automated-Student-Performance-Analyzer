from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

connection = pymysql.connect(
    host=os.getenv("MYSQL_HOST"),
    port=int(os.getenv("MYSQL_PORT")),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE"),
    ssl={"ssl": {}}
)

print("MySQL connected!")