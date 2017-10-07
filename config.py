# config
import sqlite3

IP_ADDRESS = '127.0.0.1'  # IP Address to bind
PORT = 80  # port to bind
DATABASE = 'record.db'


def end():
    '''
    this function to execute while something wrong happened
    '''
    print("bad error\n")


def sql_execute(sql_command):
    print(sql_command + "\n")
    conn = sqlite3.connect(DATABASE)  # connect to the database(using sqlite3)
    print("open database successfully")
    cur = conn.cursor()  # sql cursor, which is used to operate database
    cur.execute(sql_command)  # execute sql command
    conn.commit()  # use commit to ensure the change
    conn.close()  # close the connection


def sql_select(sql_command):
    print(sql_command + "\n")
    conn = sqlite3.connect(DATABASE)  # connect to the database(using sqlite3)
    print("open database successfully")
    cur = conn.cursor()  # sql cursor, which is used to operate database
    cur.execute(sql_command)  # execute sql command
    return cur
