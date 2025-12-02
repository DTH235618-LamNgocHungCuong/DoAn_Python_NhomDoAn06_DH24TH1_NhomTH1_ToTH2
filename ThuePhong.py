from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from SQL_connec import conn, cur
from tkinter import filedialog, messagebox

def open_ThuePhong():
   def center_window(win, w=800, h=700):
       ws = win.winfo_screenwidth()
       hs = win.winfo_screenheight()
       x = (ws // 2) - (w // 2)
       y = (hs // 2) - (h // 2)
       win.geometry(f'{w}x{h}+{x}+{y}')

   rootTP = Tk()
   rootTP.title("Thuê Phòng khách sạn")
   rootTP.minsize(800, 700)
   center_window(rootTP)

   Label(rootTP, text="THUÊ PHÒNG KHÁCH SẠN", font=("Times New Roman", 18, "bold")).pack(pady=5)

   frame = Frame(rootTP)

   Label(frame, text="Mã thuê phòng:", font=("Times New Roman", 14)).grid(row=1, column=0)
   entry_mtp = Entry(frame, width=10)
   entry_mtp.grid(row=1, column=1)

   Label(frame, text="Mã khách hàng:", font=("Times New Roman", 14)).grid(row=1, column=2)
   entry_mkh = ttk.Combobox(frame, width=10)
   entry_mkh.grid(row=1, column=3)

   Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_mnv = ttk.Combobox(frame, width=10)
   entry_mnv.grid(row=2, column=1)

   Label(frame, text="Mã phòng:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_mp = ttk.Combobox(frame, width=10)
   entry_mp.grid(row=2, column=3)

   Label(frame, text="Ngày đến:", font=("Times New Roman", 14)).grid(row=3, column=0)
   entry_nd = DateEntry (frame, width=10, date_pattern="yyyy-mm-dd")
   entry_nd.grid(row=3, column=1)

   Label(frame, text="Ngày đi:", font=("Times New Roman", 14)).grid(row=3, column=2)
   entry_ndi = DateEntry(frame, width=10, date_pattern="yyyy-mm-dd")
   entry_ndi.grid(row=3, column=3)

   Label(frame, text="Số ngày:", font=("Times New Roman", 14)).grid(row=4, column=0)
   entry_sn = Label(frame, width=10, font=("Times New Roman"))
   entry_sn.grid(row=4, column=1)

   Label(frame, text="Thành tiền:", font=("Times New Roman", 14)).grid(row=4, column=2)
   entry_tt = Label(frame, width=15, font=("Times New Roman"))
   entry_tt.grid(row=4, column=3)

   frame.pack(padx=4, pady=4, anchor="center")

   frame_bang = Frame(rootTP)
   frame_bang.pack(pady=5, expand=True)

   # Treeview
   columns = ("Mã thuê phòng", "Mã khách hàng", "Mã nhân viên", "Mã phòng", "Ngày đến", "Ngày đi", "Số ngày",
              "Thành tiền")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)

   tree.heading("Mã thuê phòng", text="Mã thuê phòng")
   tree.heading("Mã khách hàng", text="Mã khách hàng")
   tree.heading("Mã nhân viên", text="Mã nhân viên")
   tree.heading("Mã phòng", text="Mã phòng")
   tree.heading("Ngày đến", text="Ngày đến")
   tree.heading("Ngày đi", text="Ngày đi")
   tree.heading("Số ngày", text="Số ngày")
   tree.heading("Thành tiền", text="Thành tiền")

   tree.column("Mã thuê phòng", width=100, anchor="center")
   tree.column("Mã khách hàng", width=100, anchor="center")
   tree.column("Mã nhân viên", width=100, anchor="center")
   tree.column("Mã phòng", width=100, anchor="center")
   tree.column("Ngày đến", width=100)
   tree.column("Ngày đi", width=100)
   tree.column("Số ngày", width=100, anchor="center")
   tree.column("Thành tiền", width=160)

   tree.pack(padx=5, pady=10, fill="x")

   def kt_matp(matp):
       soma = len(matp)
       if soma != 6:
           return False
       if matp[0].isupper() and matp[1].isupper() and matp[2].isdigit() and matp[3].isdigit() and matp[4].isdigit() and matp[5].isdigit():
           return True
       else:
           return False

   def load_makh_combobox():
       try:
           cur.execute("select MaKH from KhachHang")
           makh_data = cur.fetchall()
           makh_list = [row[1] for row in makh_data]
           entry_mkh["values"] = makh_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã khách hàng{e}")

   def load_manv_combobox():
       try:
           cur.execute("select MaNV from NhanVien")
           manv_data = cur.fetchall()
           manv_list = [row[1] for row in manv_data]
           entry_mnv["values"] = manv_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã nhân viên{e}")

   def load_maph_combobox():
       try:
           cur.execute("select MaPh from Phong")
           maph_data = cur.fetchall()
           maph_list = [row[1] for row in maph_data]
           entry_mp["values"] = maph_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã phòng{e}")

   def tinh_songay_va_thanhtien():
       try:
           ngayden = entry_nd.get()
           ngaydi = entry_ndi.get()
           if ngaydi <= ngayden:
                messagebox.showwarning("Số ngày đi phải lớn hơn ngày đến", "Vui lòng nhập lại thông tin")
                return None, None
           songay = (ngaydi - ngayden).days
           maph = entry_mp.get()
           cur.execute("select GiaPh from Phong where MaPh = %s", (maph,))
           maph_data = cur.fetchall()
           if not maph_data:
                messagebox.showwarning("Không tìm thấy mã phòng", "Vui lòng nhập lại thông tin")
                return None, None
           gia = float(maph_data[0])
           thanhtien = gia * songay
           return songay, thanhtien
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi tính thành tiền{e}")
           return None, None

   def hien_songay_va_thanhtien():
       ngden = entry_nd.get()
       ngdi = entry_ndi.get()
       if ngden != "" and ngdi != "":
           songay, thanhtien = tinh_songay_va_thanhtien()
           if songay is not None and thanhtien is not None:
               entry_nd.config(text=str(songay))
               entry_ndi.config(text=str(thanhtien))



   def clear_input():
       entry_mtp.delete(0, END)
       entry_mkh.delete(0, END)
       entry_mnv.delete(0, END)
       entry_mp.delete(0, END)
       entry_nd.delete(0, END)
       entry_ndi.delete(0, END)
       entry_sn.config(text="")
       entry_tt.config(text="")

   def load_data():

       if conn is None or cur is None:
           messagebox.showerror("Lỗi", "Không thể kết nối với SQL.")
           return
       tree.delete(*tree.get_children())
       try:
           cur.execute("SELECT * FROM ThuePhong")
           for row in cur.fetchall():
               tree.insert("", END, values=row)
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")

   def them_TP():
       matp = entry_mtp.get()
       makh = entry_mkh.get()
       manv = entry_mnv.get()
       maph = entry_mp.get()
       ngden = entry_nd.get()
       ngdi = entry_ndi.get()

       if matp == "" or makh == "" or manv == "" or maph == "" or ngden == "" or ngdi == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_matp(matp) == False:
           messagebox.showerror("Lỗi", "MaTP không hợp lệ")
           return

       songay, thanhtien = tinh_songay_va_thanhtien()
       if songay is None or thanhtien is None:
           return

       try:
           # kt xem tang có bị trùng ko
           cur.execute("SELECT COUNT(*) FROM ThuePhong where MaTP = %s", (matp,))

           if cur.fetchone()[0] > 0:
               messagebox.showwarning("Trùng lập", f"Mã thuê phòng {matp} đã tồn tại")
               return

           cur.execute("Insert into ThuePhong (MaTP, MaKH, MaNV, MaPh, NgDen, NgDi, SoNgay, ThanhTien) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                       (matp,makh,manv,maph,ngden,ngdi,songay,thanhtien))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Đã thêm thuê phòng")
       except Exception as e:
           messagebox.showerror("Lỗi", f"{e}")

   def xoa_TP():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
           return
       matp = tree.item(selected, "values")[0]
       confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?")
       if not confirm:
           return

       try:
           cur.execute("DELETE FROM ThuePhong where MaTP=%s", (matp,))
           conn.commit()
           load_data()
           messagebox.showinfo("Đã xoá")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")

   def sua_TP():
       selected = tree.selection()
       if not selected:
           messagebox.showwarning("Chưa chọn", "Hãy chọn 1 dòng để sửa")
           return
       values = tree.item(selected)["values"]
       entry_mtp.delete(0, END)
       entry_mtp.insert(0, values[0])
       entry_mtp.config(state='disabled')
       entry_mkh.delete(0, END)
       entry_mkh.insert(0, values[1])
       entry_mnv.delete(0, END)
       entry_mnv.insert(0, values[2])
       entry_mp.delete(0, END)
       entry_mp.insert(0, values[3])
       entry_nd.set_date(values[4])
       entry_ndi.set_date(values[5])
       entry_sn.config(text=values[6])
       entry_tt.config(text=values[7])

       matp = entry_mtp.get()
       makh = entry_mkh.get()
       manv = entry_mnv.get()
       maph = entry_mp.get()
       ngden = entry_nd.get()
       ngdi = entry_ndi.get()

       if matp == "" or makh == "" or manv == "" or maph == "" or ngden == "" or ngdi == "":
           messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
           return

       if kt_matp(matp) == False:
           messagebox.showerror("Lỗi", "MaTP không hợp lệ")
           return

       songay, thanhtien = tinh_songay_va_thanhtien()
       if songay is None or thanhtien is None:
           return

   def luu_TP():
       matp = entry_mtp.get()
       makh = entry_mkh.get()
       manv = entry_mnv.get()
       maph = entry_mp.get()
       ngden = entry_nd.get()
       ngdi = entry_ndi.get()

       songay, thanhtien = tinh_songay_va_thanhtien()
       if songay is None or thanhtien is None:
           return

       try:
           cur.execute(
               """UPDATE ThuePhong SET MaTP=%s, MaKH=%s, MaNV=%s, MaPh=%s, NgDen=%s, NgDi=%s, SoNgay=%s, ThanhTien=%s""",
               (matp, makh, manv, maph, ngden, ngdi, songay, ngdi))
           conn.commit()
           load_data()
           clear_input()
           messagebox.showinfo("Thành công", "Cập nhật thành công.")
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi khi lưu:\n{e}")

   frame_btn = Frame(rootTP)
   frame_btn.pack(padx=5, pady=5, anchor="center")

   Button(frame_btn, text="Thêm", width=8, command=them_TP).grid(row=0, column=0, padx=5)
   Button(frame_btn, text="Lưu", width=8, command=luu_TP).grid(row=0, column=1, padx=5)
   Button(frame_btn, text="Sửa", width=8, command=sua_TP).grid(row=1, column=0, padx=5)
   Button(frame_btn, text="Xoá", width=8, command=xoa_TP).grid(row=1, column=1, padx=5)
   Button(frame_btn, text="Thoát", width=8, command=rootTP.quit).grid(row=0, column=2, padx=5)

   load_data()
   load_makh_combobox()
   load_maph_combobox()
   load_manv_combobox()
   hien_songay_va_thanhtien()

   rootTP.mainloop()
