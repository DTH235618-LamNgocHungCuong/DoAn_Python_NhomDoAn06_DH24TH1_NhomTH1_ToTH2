from tkinter import *
from tkinter import ttk, messagebox, filedialog
import datetime
import os
import pyodbc
#from tkcalendar import DateEntry
#import mysql.connector

'''
def connect_db():
   try:
       conn = pyodbc.connect(
           "DRIVER={ODBC Driver 17 for SQL Server};"
           "SERVER=DESKTOP-69RCC7P;"
           "DATABASE=QLKS_DA;"
           "UID=sa;" # Thay bằng user SQL
           "PWD=123;" # Thay bằng password SQL
           "Trusted_Connection=yes;"
       )
       print("Kết nối thành cong.")
       return conn
   except Exception as err:
       print("Lỗi kết nối MySQL:", err)
       return None
'''

def connect_db():
    try:
        conn = pyodbc.connect(
            "DRIVER={ODBC Driver 17 for SQL Server};"
            "SERVER=KATORIDESU;"
            "DATABASE=QLKS_DA;"
            "Trusted_Connection=yes;"
        )
        print("Kết nối SQL Server thành công (Windows Authentication).")
        return conn
    except Exception as err:
        print("Lỗi kết nối SQL Server:", err)
        return None


def get_all_codes(table_name, code_column):
    conn = connect_db()
    if not conn: return []
    cur = conn.cursor()
    codes = []
    try:
        cur.execute(f"SELECT {code_column} FROM {table_name}")
        codes = [row[0].strip() for row in cur.fetchall()]
    except Exception as e:
        print(f"Lỗi khi lấy mã {code_column} từ {table_name}: {e}")
    finally:
        if conn: conn.close()
    return codes

