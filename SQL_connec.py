from tkinter import *
from tkinter import ttk, messagebox
#import pyodbc
#from tkcalendar import DateEntry
#import mysql.connector
'''
def connect_db():
   try:
       conn = pyodbc.connect(
           "DRIVER={ODBC Driver 17 for SQL Server};"
           "SERVER=lLIB-SV304\SQL;"
           "DATABASE=QLKS_DA;"
           "Trusted_Connection=no;"
       )
       print("Kết nối thành cngg.")
       return conn
   except Exception as err:
       print("Lỗi kết nối MySQL:", err)
       return None




def connect_db():
   try:
       conn =  mysql.connector.connect(
           host="localhost",
           user="root",  # thay bằng user MySQL của bạn
           password= "",  # thay bằng password MySQL của bạn
           database="qlnhanvien"
       )
       print("Kết nối thành cngg.")
       return conn
   except mysql.connector.Error as err:
       print("Lỗi kết nối MySQL:", err)
       return None




conn = connect_db()
if conn:
   cur = conn.cursor()
else:
   cur = None
'''
