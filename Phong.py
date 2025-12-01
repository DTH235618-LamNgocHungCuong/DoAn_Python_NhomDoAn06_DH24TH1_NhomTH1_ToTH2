from tkinter import *
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
#from SQL_connec import conn, cur
from tkinter import filedialog, messagebox

def open_Phong():
   def center_window(win, w=800, h=600):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootP = Tk()
   rootP.title("Quản lý Tầng")
   rootP.minsize(800, 600)
   center_window(rootP)

   Label(rootP, text="QUẢN LÝ PHÒNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootP)

   Label(frame, text="Mã phòng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mp = Entry(frame, width=10)
   entry_mp.grid(row=1, column=1)

   Label(frame, text="Loại phòng:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_lp = ttk.Combobox(frame, width=10, values=["Giường Đơn", "Giường Đôi", "Phòng gia đình"])
   entry_lp.grid(row=1, column=3)

   Label(frame, text="Giá phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_gp = Entry(frame, width=10)
   entry_gp.grid(row=2, column=1)

   Label(frame, text="Tầng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_st = ttk.Combobox(frame, width=10, state="readonly")
   entry_st.grid(row=1, column=1)

   frame.pack(padx=5, pady=4, anchor="center")



   frame_bang = Frame(rootP)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Mã phòng", "Loại phòng", "Giá phòng", "Tầng")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)
   for col in columns:
       tree.heading(col, text=col.title())

   tree.column("Mã phòng", width=60, anchor="center")
   tree.column("Loại Phòng", width=150)
   tree.column("Giá Phòng", width=150)
   tree.column("Tầng", width=60, anchor="center")

   tree.pack(padx=5, pady=10, fill="x")

   def kt_sTang(tang):
       if tang>=0 and tang<=20:
           return True
       else:
           return False

   def kt_maph(maph):
       soma = len(maph)
       if soma != 5:
           return False
       if maph[0].isupper() and maph[1].isupper() and maph[2].isdigit() and maph[3].isdigit() and maph[4].isdigit():
           return True
       else:
           return False


   def load_tang_combobox():
       try:
           cur.execute("select * from Tang")
           tang_data = cur.fetchall()
           tang_list = [row[1] for row in tang_data]
           entry_st["values"] = tang_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load số tầng{e}")

   def clear_input():
       entry_st.delete(0, END)
       entry_lp.delete(0, END)
       entry_gp.delete(0, END)
       entry_st.delete(0, END)

   def load_data():
       '''
       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM Phong")
           for row in cur.fetchall():
               tree.insert("", END, values=row)
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
       '''

   def them_phong():
       maph = entry_st.get()
       loaiphong = entry_lp.get()
       giaphong = entry_gp.get()
       tang = entry_st.get()

       if maph == "" or loaiphong == "" or giaphong == "" or tang == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_maph(maph) == False:
           messagebox.showerror("Lỗi","MaPh không hợp lệ")
           return


       try:
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM Phong where MaPh = %s", (maph,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Phòng {maph} đã tồn tại")
               return

           cur.execute("Insert into Phong (MaPh, LoaiPh, GiaPh, Tang) VALUES (%s, %s, %s, %s)", (maph, loaiphong,giaphong,tang))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm phòng mới")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")




