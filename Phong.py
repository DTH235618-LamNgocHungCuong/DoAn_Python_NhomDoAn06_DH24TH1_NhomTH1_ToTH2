from tkinter import *
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
from SQL_connec import conn, cur
from tkinter import filedialog, messagebox

def open_Phong():
   def center_window(win, w=800, h=700):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootP = Tk()
   rootP.title("Quản lý Tầng")
   rootP.minsize(800, 700)
   center_window(rootP)

   Label(rootP, text="QUẢN LÝ PHÒNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootP)

   Label(frame, text="Mã phòng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mp = Entry(frame, width=10)
   entry_mp.grid(row=1, column=1)

   Label(frame, text="Loại phòng:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_lp = ttk.Combobox(frame, width=10, values=["Đơn", "Đôi", "Giađình"])
   entry_lp.grid(row=1, column=3)

   Label(frame, text="Giá phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_gp = Entry(frame, width=10)
   entry_gp.grid(row=2, column=1)

   Label(frame, text="Tầng:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_st = ttk.Combobox(frame, width=10, state="readonly")
   entry_st.grid(row=2, column=3)



   frame.pack(padx=4, pady=4, anchor="center")



   frame_bang = Frame(rootP)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Mã_phòng", "Loại_phòng", "Giá_phòng", "Tầng")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)
   
   tree.heading("Mã_phòng", text="Mã_phòng")
   tree.heading("Loại_phòng", text="Loại_phòng")
   tree.heading("Giá_phòng", text="Giá_phòng")
   tree.heading("Tầng", text="Tầng")
   
   tree.column("Mã_phòng", width=60, anchor="center")
   tree.column("Loại_phòng", width=150)
   tree.column("Giá_phòng", width=150)
   tree.column("Tầng", width=60, anchor="center")
   
   tree.pack(padx=5, pady=10, fill="x")

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
           tang_list = [row[0] for row in tang_data]
           entry_st["values"] = tang_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load số tầng {e}")
       

   def clear_input():
       entry_mp.delete(0, END)
       entry_lp.set("")
       entry_gp.delete(0, END)
       entry_st.set("")

   def load_data():
       
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
       

   def them_phong():
       maph = entry_mp.get()
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
           cur.execute("SELECT COUNT(*) FROM Phong where MaPh = ?", (maph,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Phòng {maph} đã tồn tại")
               return

           cur.execute("Insert into Phong (MaPh, LoaiPh, GiaPh, Tang) VALUES (?, ?, ?, ?)", (maph, loaiphong,giaphong,tang))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm phòng mới")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")
       

   def xoa_phong():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       phong = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?")
       if not confirm:
           return
       
       try:
           cur.execute("DELETE FROM Phong where MaPh=?", (phong,))
           conn.commit()
           load_data()
           messagebox.showinfo("Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")
       

   def sua_phong():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn loại phòng để sửa")
           return
       values = tree.item(selected)["values"]
       entry_mp.delete(0, END)
       entry_mp.insert(0, values[0]) #khóa
       entry_mp.config(state='disabled')
       entry_lp.set(values[1])
       entry_gp.delete(0, END)
       entry_gp.insert(0, values[2])
       entry_st.set(values[3])

       maph = entry_mp.get()
       loaiphong = entry_lp.get()
       giaphong = entry_gp.get()
       tang = entry_st.get()

       if maph == "" or loaiphong == "" or giaphong == "" or tang == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_maph(maph) == False:
           messagebox.showerror("Lỗi","MaPh không hợp lệ")
           return
       
   def luu_phong():
       maph = entry_mp.get()
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
           cur.execute("""UPDATE Phong SET LoaiPh=?, GiaPh=?, Tang=? where MaPh=?""", (loaiphong,giaphong,tang,maph))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")
       

   frame_btn = Frame(rootP)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_phong).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_phong).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_phong).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_phong).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=rootP.quit).grid(row=0, column=2, padx=5)

   

   load_data()
   load_tang_combobox()

   rootP.mainloop()



