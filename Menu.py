from tkinter import *
from tkinter import messagebox
#from tkcalendar import DateEntry
from SQL_connec import conn, cur
from Tang import open_Tang
from Phong import open_Phong
from KhachHang import open_KhachHang


def mo_menu(quyen):
   def center_window(win, w=700, h=500):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')


   rootM = Tk()
   rootM.title("Menu Quản lý khách sạn")
   rootM.minsize(width = 700, height = 700)
   center_window(rootM)


   Label(rootM, text="MENU QUẢN LÝ KHÁCH SẠN",font=("Times New Roman", 18, "bold")).pack(pady=5, anchor = CENTER)


   aButton = Frame (rootM)
   Button(aButton, text="Tầng", font=("Times New Roman", 14), width=8, command=lambda: open_Tang()).grid(row=1, column=0)
   Button(aButton, text="Phòng", font=("Times New Roman", 14), width=8, command=lambda: open_Phong()).grid(row=1, column=1)
   Button(aButton, text="Khách Hàng", font=("Times New Roman", 14), width=8, command=lambda: open_KhachHang()).grid(row=1, column=2)

   aButton.pack(padx=5, pady=5, anchor = "center")


   rootM.mainloop()
