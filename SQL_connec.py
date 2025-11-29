from tkinter import *
from tkinter import ttk, messagebox
import pyodbc


def connect_db():
	try:
		conn = pyodbc.connect (
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
	
conn = connect_db()
if conn:
	cur = conn.cursor()
else:
	cur = None