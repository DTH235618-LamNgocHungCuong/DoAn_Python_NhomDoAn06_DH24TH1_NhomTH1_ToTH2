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

   rootNV = Tk()
   rootNV.title("Quản lý Khách Hàng")
   rootNV.minsize(900, 700)
   center_window(rootNV)

   Label(rootNV, text="QUẢN LÝ NHÂN VIÊN", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootNV)

   Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mnv = Entry(frame, width=10)
   entry_mnv.grid(row=1, column=1)

   Label(frame, text="Tên nhân viên:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_tnv = Entry(frame, width=15)
   entry_tnv.grid(row=1, column=3)

   Label(frame, text="Giới tính:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_gt = Entry(frame, width=15)
   entry_gt.grid(row=2, column=1)

   Label(frame, text="Điện thoại:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_dt = Entry(frame, width=15)
   entry_dt.grid(row=2, column=3)

   Label(frame, text="Địa chỉ:", font=("Times New Roman", 14)).grid(row=3, column=0)
   entry_dc = Entry(frame, width=15)
   entry_dc.grid(row=3, column=1)

   Label(frame, text="Chức vụ:", font=("Times New Roman", 14)).grid(row=3, column=2)
   entry_cv = Entry(frame, width=15)
   entry_cv.grid(row=3, column=3)

   Label(frame, text="Tầng trực:", font=("Times New Roman", 14)).grid(row=4, column=0)
   entry_tt = ttk.Combobox(frame, width=10, state="readonly")
   entry_tt.grid(row=4, column=1)

   Label(frame, text="Mật khẩu:", font=("Times New Roman", 14)).grid(row=4, column=2)
   entry_mk = Entry(frame, width=15)
   entry_mk.grid(row=4, column=3)

   frame.pack(padx=4, pady=4, anchor="center")

   frame_bang = Frame(rootNV)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Mã nhân viên", "Tên nhân viên", "Giới tính", "Điện thoại", "Địa chỉ", "Chức vụ", "Tầng trực", "Mật khẩu")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)

   tree.heading("Mã nhân viên", text="Mã nhân viên")
   tree.heading("Tên nhân viên", text="Tên nhân viên")
   tree.heading("Giới tính", text="Giới tính")
   tree.heading("Điện thoại", text="Điện thoại")
   tree.heading("Địa chỉ", text="Địa chỉ")
   tree.heading("Chức vụ", text="Chức vụ")
   tree.heading("Tầng trực", text="Tầng trực")
   tree.heading("Mật khẩu", text="Mật khẩu")

   tree.column("Mã nhân viên", width=100, anchor="center")
   tree.column("Tên nhân viên", width=150)
   tree.column("Giới tính", width=100)
   tree.column("Điện thoại", width=100)
   tree.column("Địa chỉ", width=150)
   tree.column("Chức vụ", width=150)
   tree.column("Tầng trực", width=100, anchor="center")
   tree.column("Mật khẩu", width=150)

   tree.pack(padx=5, pady=10, fill="x")

   def kt_manv(manv):
       soma = len(manv)
       if soma != 5:
           return False
       if manv[0].isupper() and manv[1].isdigit() and manv[2].isupper() and manv[3].isdigit() and manv[4].isdigit():
           return True
       else:
           return False

   def load_tangt_combobox():
       try:
           cur.execute("select * from Tang")
           tang_data = cur.fetchall()
           tang_list = [row[1] for row in tang_data]
           entry_tt["values"] = tang_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load số tầng{e}")

   def clear_input():
       entry_mnv.delete(0, END)
       entry_tnv.delete(0, END)
       entry_gt.delete(0, END)
       entry_dt.delete(0, END)
       entry_dc.delete(0, END)
       entry_cv.delete(0, END)
       entry_tt.delete(0, END)
       entry_mk.delete(0, END)

   def load_data():
       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM NhanVien")
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

   def them_NV():
       manv = entry_mnv.get()
       tennv = entry_tnv.get()
       gioitinh = entry_gt.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()
       chucvu = entry_cv.get()
       tangtruc = entry_tt.get()
       matkhau = entry_mk.get()

       if manv == "" or tennv == "" or gioitinh == "" or dthoai == "" or dchi == "" or chucvu == "" or tangtruc == "" or matkhau == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_manv(manv) == False:
           messagebox.showerror("Lỗi", "MaKH không hợp lệ")
           return

       try:
           manv = suaten(manv)
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM NhanVien where MaNV = %s", (manv,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Nhân viên {manv} đã tồn tại")
               return

           cur.execute("Insert into NhanViên (MaNV, TenNV, GioiTinhNV, DThoaiNV, DChiKH, ChucVu, TangTruc, MatKhau) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (manv,tennv,gioitinh,dthoai,dchi,chucvu,tangtruc,matkhau))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm phòng mới")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")

   def xoa_NV():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       manv = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?")
       if not confirm:
           return

       try:
           cur.execute("DELETE FROM NhanVien where MaNV=%s", (manv,))
           conn.commit()
           load_data()
           messagebox.showinfo("Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")

   def sua_NV():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để sửa")
           return
       values = tree.item(selected)["values"]
       entry_mnv.delete(0, END)
       entry_mnv.insert(END, values[0])
       entry_mnv.config(state='disabled')
       entry_tnv.delete(0, END)
       entry_tnv.insert(END, values[1])
       entry_gt.delete(0, END)
       entry_gt.insert(END, values[2])
       entry_dt.delete(0, END)
       entry_dt.insert(END, values[3])
       entry_dc.delete(0, END)
       entry_dc.insert(END, values[4])
       entry_cv.delete(0, END)
       entry_cv.insert(END, values[5])
       entry_tt.delete(0, END)
       entry_tt.insert(END, values[6])
       entry_mk.delete(0, END)
       entry_mk.insert(END, values[7])

       manv = entry_mnv.get()
       tennv = entry_tnv.get()
       gioitinh = entry_gt.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()
       chucvu = entry_cv.get()
       tangtruc = entry_tt.get()
       matkhau = entry_mk.get()

       if manv == "" or tennv == "" or gioitinh == "" or dthoai == "" or dchi == "" or chucvu == "" or tangtruc == "" or matkhau == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_manv(manv) == False:
           messagebox.showerror("Lỗi", "MaKH không hợp lệ")
           return

   def luu_NV():
       manv = entry_mnv.get()
       tennv = entry_tnv.get()
       gioitinh = entry_gt.get()
       dthoai = entry_dt.get()
       dchi = entry_dc.get()
       chucvu = entry_cv.get()
       tangtruc = entry_tt.get()
       matkhau = entry_mk.get()

       manv = suaten(manv)

       try:
           cur.execute("""UPDATE NhanVien SET MaNV=%s, TenNV=%s, GioiTinhNV=%s, DThoaiNV=%s, DChiNV=%s, ChucVu=%s, TangTruc=%s, MatKhau=%s""",
                       (manv, tennv, gioitinh, dthoai, dchi, chucvu, tangtruc, matkhau))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")

   frame_btn = Frame(rootNV)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_NV).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_NV).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_NV).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_NV).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=rootNV.quit).grid(row=0, column=2, padx=5)

   load_data()
   load_tangt_combobox()

   rootNV.mainloop()
