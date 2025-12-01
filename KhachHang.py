from tkinter import *
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
from SQL_connec import conn, cur
from tkinter import filedialog, messagebox

def open_KhachHang():
   def center_window(win, w=900, h=700):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootKH = Tk()
   rootKH.title("Quản lý Khách Hàng")
   rootKH.minsize(900, 700)
   center_window(rootKH)

   Label(rootKH, text="QUẢN LÝ KHÁCH HÀNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootKH)

   Label(frame, text="Mã khách hàng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mkh = Entry(frame, width=10)
   entry_mkh.grid(row=1, column=1)

   Label(frame, text="Tên khách hàng:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_tkh = Entry(frame, width=15)
   entry_tkh.grid(row=1, column=3)

   Label(frame, text="Điện thoại:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_dt = Entry(frame, width=15)
   entry_dt.grid(row=2, column=1)

   Label(frame, text="Địa chỉ:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_dc = Entry(frame, width=15)
   entry_dc.grid(row=2, column=3)


   frame.pack(padx=4, pady=4, anchor="center")



   frame_bang = Frame(rootKH)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Mã khách hàng", "Tên khách hàng", "Điện thoại", "Địa chỉ")  # cần dấu phẩy ở cuối
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
       tree.column(col, width=150, anchor="center")

   tree.pack(padx=5, pady=10, fill="x")

   def kt_makh(makh):
       soma = len(makh)
       if soma != 4:
           return False
       if makh[0].isupper() and makh[1].isdigit() and makh[2].isdigit() and makh[3].isdigit():
           return True
       else:
           return False


   def clear_input():
       entry_mkh.delete(0, END)
       entry_tkh.delete(0, END)
       entry_dt.delete(0, END)
       entry_dc.delete(0, END)

   def load_data():
       
       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM KhachHang")
           for row in cur.fetchall():
               tree.insert("", END, values=row)
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
       
   def suaten(tenkh):
       s = tenkh
       s = s.strip()
       arr = s.split(' ')
       s = ""
       for i in arr:
           word = i
           if len(word.strip()) != 0:
               s += word + "_"
       return s.strip()


   def them_KH():
       makh = entry_mkh.get()
       tenkh = entry_tkh.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()

       if makh == "" or tenkh == "" or dthoai == "" or dchi == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_makh(makh) == False:
           messagebox.showerror("Lỗi","MaKH không hợp lệ")
           return


       try:
           makh = suaten(makh)
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM KhachHang where MaKH = %s", (makh,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Phòng {makh} đã tồn tại")
               return

           cur.execute("Insert into KhachHang (MaKH, TenKH, DThoaiKH, DChiKH) VALUES (%s, %s, %s, %s)", (makh, tenkh,dthoai,dchi))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm phòng mới")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")

   def xoa_KH():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       makh = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?")
       if not confirm:
           return
       
       try:
           cur.execute("DELETE FROM KhachHang where MaKH=%s", (makh,))
           conn.commit()
           load_data()
           messagebox.showinfo("Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")

   def sua_KH():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn loại phòng để sửa")
           return
       values = tree.item(selected)["values"]
       entry_mkh.delete(0, END)
       entry_mkh.insert(0, values[0]) #khóa
       entry_mkh.config(state='disabled')
       entry_tkh.delete(0, END)
       entry_tkh.config(0, values[1])
       entry_dt.delete(0, END)
       entry_dt.insert(0, values[2])
       entry_dc.delete(0, END)
       entry_dc.insert(0, values[3])

       makh = entry_mkh.get()
       tenkh = entry_tkh.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()

       if makh == "" or tenkh == "" or dthoai == "" or dchi == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_makh(makh) == False:
           messagebox.showerror("Lỗi","MaPh không hợp lệ")
           return
       
   def luu_KH():
       makh = entry_mkh.get()
       tenkh = entry_tkh.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()

       makh = suaten(makh)
      
       try:
           cur.execute("""UPDATE KhachHang SET MaKH=%s, TenKH=%s, DThoaiKH=%s, DChiKH=%s""", (makh,tenkh,dthoai,dchi))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")

   frame_btn = Frame(rootKH)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_KH).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_KH).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_KH).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_KH).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=rootKH.quit).grid(row=0, column=2, padx=5)

   

   load_data()

   rootKH.mainloop()