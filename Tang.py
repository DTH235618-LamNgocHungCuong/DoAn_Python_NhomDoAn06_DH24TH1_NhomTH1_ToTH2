from tkinter import *
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
#from SQL_connec import conn, cur
from tkinter import filedialog, messagebox

def open_Tang():
   def center_window(win, w=450, h=450):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootT = Tk()
   rootT.title("Quản lý Tầng")
   rootT.minsize(450, 450)
   center_window(rootT)

   Label(rootT, text="QUẢN LÝ TẦNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootT)

   Label(frame, text="Số tầng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_st = Entry(frame, width=10)
   entry_st.grid(row=1, column=1)

   frame.pack(padx=5, pady=4, anchor="center")

   frame_bang = Frame(rootT)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Tầng",) #cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=9)

   # Thanh cuộn
   scroll_bar = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   tree.configure(yscrollcommand=scroll_bar.set)

   scroll_bar.pack(side="right", fill="y")
   tree.pack(side="left", expand=True)
   for col in columns:
       tree.heading(col, text=col.title())

   tree.column ("Tầng", width=60, anchor="center")

   tree.pack(padx=5, pady=10, fill="x")

   def kt_sTang(tang):
       if tang>=0 and tang<=20:
           return True
       else:
           return False

   def clear_input():
       entry_st.delete(0, END)

   def load_data():
       '''
       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM Tang")
           for row in cur.fetchall():
               tree.insert("", END, values=row)
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
       '''

   def them_tang():
       tang = entry_st.get()

       if tang == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_sTang(int(tang))==False:
           messagebox.showwarning("Số tầng không đúng quy định", "Vui lòng nhập lại thông tin")
           return

       '''
       try:
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM Tang where Tang = %s", (tang,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Tầng {tang} đã tồn tại")
               return

           cur.execute("Insert into Tang (tang) VALUES (%s)", (tang))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm tầng mới")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")
       '''

   def xoa_tang():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       tang = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa loại phòng?")
       if not confirm:
           return
       '''
       try:
           cur.execute("DELETE FROM Tang where Tang=%s", (tang,))
           conn.commit()
           load_data()
           messagebox.showinfo("Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")
       '''

   def sua_tang():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn loại phòng để sửa")
           return
       values = tree.item(selected)["values"]
       entry_st.delete(0, END)
       entry_st.insert(0, values[0])

       tang = entry_st.get()

       if tang == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_sTang(int(tang)) == False:
           messagebox.showwarning("Số tầng không đúng quy định", "Vui lòng nhập lại thông tin")
           return

   def luu_tang():
       tang = entry_st.get()

       '''
       try:
           cur.execute("""UPDATE Tang SET Tang=%s""", (tang))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")
       '''

   frame_btn = Frame(rootT)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_tang).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_tang).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_tang).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_tang).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=rootT.quit).grid(row=0, column=2, padx=5)

   rootT.mainloop()

