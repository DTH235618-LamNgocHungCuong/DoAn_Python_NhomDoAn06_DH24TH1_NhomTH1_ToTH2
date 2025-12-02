from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from SQL_connec import conn, cur
from tkinter import filedialog, messagebox
from Menu import mo_menu

def open_HoaDon():
   def center_window(win, w=800, h=700):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootHD = Tk()
   rootHD.title("Hoá đơn")
   rootHD.minsize(800, 700)
   center_window(rootHD)

   Label(rootHD, text="QUẢN LÝ HOÁ ĐƠN", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootHD)

   Label(frame, text="Mã hoá đơn:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mhd = Entry(frame, width=10)
   entry_mhd.grid(row=1, column=1)

   Label(frame, text="Mã khách hàng:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_mkh = Label(frame, width=10, font=("Times New Roman", 14))
   entry_mkh.grid(row=1, column=3)

   Label(frame, text="Mã thuê phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_mtp = ttk.Combobox(frame, width=10)
   entry_mtp.grid(row=2, column=1)

   Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_mnv = ttk.Combobox(frame, width=10)
   entry_mnv.grid(row=2, column=3)

   Label(frame, text="Tổng tiền:", font=("Times New Roman", 14)).grid(row=3, column=0)
   entry_tot = Label(frame, width=15, font=("Times New Roman", 14))
   entry_tot.grid(row=3, column=1)

   frame.pack(padx=4, pady=4, anchor="center")

   frame_bang = Frame(rootHD)
   frame_bang.pack(pady=5, expand=True)

   columns = ("Mã_hoá_đơn", "Mã_khách_hàng", "Mã_thuê_phòng", "Mã_nhân_viên", "Tổng_tiền")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)

   tree.heading("Mã_hoá_đơn", text="Mã_hoá_đơn")
   tree.heading("Mã_khách_hàng", text="Mã_khách_hàng")
   tree.heading("Mã_thuê_phòng", text="Mã_thuê_phòng")
   tree.heading("Mã_nhân_viên", text="Mã_nhân_viên")
   tree.heading("Tổng_tiền", text="Tổng_tiền")

   tree.column("Mã_hoá_đơn", width=100, anchor="center")
   tree.column("Mã_khách_hàng", width=100, anchor="center")
   tree.column("Mã_thuê_phòng", width=100, anchor="center")
   tree.column("Mã_nhân_viên", width=100, anchor="center")
   tree.column("Tổng_tiền", width=100, anchor="center")

   tree.pack(padx=5, pady=10, fill="x")

   def kt_mahd(mahd):
       soma = len(mahd)
       if soma != 6:
           return False
       if mahd[0].isupper() and mahd[1].isupper() and mahd[2].isdigit() and mahd[3].isdigit() and mahd[4].isdigit() and mahd[5].isdigit():
           return True
       else:
           return False

   def load_manv_combobox():
       
       try:
           cur.execute("select MaNV from NhanVien")
           manv_data = cur.fetchall()
           manv_list = [row[0] for row in manv_data]
           entry_mnv["values"] = manv_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã nhân viên{e}")
       

   def load_matp_combobox():
       
       try:
           cur.execute("select MaTP from ThuePhong")
           matp_data = cur.fetchall()
           matp_list = [row[0] for row in matp_data]
           entry_mtp["values"] = matp_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã nhân viên{e}")       

   def lay_thanhtien_va_makh_tu_thuephong():
       
       try:
           matp = entry_mtp.get()
           cur.execute("SELECT ThanhTien, MaKH FROM ThuePhong WHERE MaTP = ?", (matp,))
           matp_data = cur.fetchall()

           if not matp_data:
                messagebox.showwarning("Không tìm thấy mã thuê phòng", "Vui lòng nhập lại thông tin")
                return None, None
           
           tongtien = float(matp_data[0][0])
           makh = matp_data[0][1]

           return tongtien, makh
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi tính tổng tiền{e}")
           return None, None
       

   def hien_tongtien_va_makh():
       matp = entry_mtp.get()
       if matp != "":
           tongtien, makh = lay_thanhtien_va_makh_tu_thuephong()
           if tongtien is not None or makh is not None:
               entry_tot.config(text=str(tongtien))
               entry_mkh.config(text=str(makh))

   def clear_input():
       entry_mhd.delete(0, END)
       entry_mkh.config(text="")
       entry_mtp.set("")
       entry_mnv.set("")
       entry_tot.config(text="")

   def load_data():
       
       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM HoaDon")
           for row in cur.fetchall():
               tree.insert("", "end", values=row)
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
       

   def them_HD():
       mahd = entry_mhd.get()
       matp = entry_mtp.get()
       manv = entry_mnv.get()

       if mahd == "" or matp == "" or manv == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_mahd(mahd) == False:
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       tongtien, makh = lay_thanhtien_va_makh_tu_thuephong()
       if tongtien is None and makh is None:
           return
       
       try:
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM HoaDon where MaHD = ?", (mahd,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Hoá đơn {mahd} đã tồn tại")
               return

           cur.execute("Insert into HoaDon (MaHD, MaKH, MaTP, MaNV, TongTien) VALUES (?, ?, ?, ?, ?)",
                       (mahd, makh, matp, manv,tongtien))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm hoá đơn")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")
       

   def xoa_HD():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       mahd = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?")
       if not confirm:
           return
       
       try:
           cur.execute("DELETE FROM HoaDon where MaHD=?", (mahd,))
           conn.commit()
           load_data()
           messagebox.showinfo("Thành công", "Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")
       

   def sua_HD():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa")
           return
       values = tree.item(selected)["values"]
       entry_mhd.delete(0, END)
       entry_mhd.insert(0, values[0])
       entry_mhd.config(state='disabled')
       entry_mkh.config(text=values[1])
       entry_mtp.set(values[2])
       entry_mnv.set(values[3])
       entry_tot.config(text=values[4])

       mahd = entry_mhd.get()
       matp = entry_mtp.get()
       manv = entry_mnv.get()

       if mahd == "" or matp == "" or manv == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_mahd(mahd) == False:
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       tongtien, makh = lay_thanhtien_va_makh_tu_thuephong()
       if tongtien is None and makh is None:
           return

   def luu_HD():
       mahd = entry_mhd.get()
       matp = entry_mtp.get()
       manv = entry_mnv.get()

       tongtien, makh = lay_thanhtien_va_makh_tu_thuephong()
       if tongtien is None and makh is None:
           return
       
       try:
           cur.execute(
               """UPDATE HoaDon SET MaKH=?, MaTP=?, MaNV=?, TongTien=? where MaHD=?""",
               (makh, matp, manv, tongtien, mahd))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")
       
   def thoat_HD():
       rootHD.destroy()
       mo_menu()

   frame_btn = Frame(rootHD)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_HD).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_HD).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_HD).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_HD).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=thoat_HD).grid(row=0, column=2, padx=5)
   
   load_data()
   load_matp_combobox()
   load_manv_combobox()
   hien_tongtien_va_makh()
   
   rootHD.mainloop()
  
  
