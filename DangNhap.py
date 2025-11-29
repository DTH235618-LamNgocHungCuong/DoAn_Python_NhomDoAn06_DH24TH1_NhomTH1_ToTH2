from tkinter import *
from tkinter import messagebox
from SQL_connec import conn, cur, connect_db
import pyodbc


def center_window(win, w = 500, h = 500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')


rootDN = Tk()
rootDN.title("Đăng nhập")
rootDN.minsize(width=400,height=400)
center_window(rootDN)


rootDN.mainloop()