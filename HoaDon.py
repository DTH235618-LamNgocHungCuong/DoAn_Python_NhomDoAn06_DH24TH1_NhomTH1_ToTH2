from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
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
   entry_mkh = Label(frame, width=10, font=("Times New Roman"))
   entry_mkh.grid(row=1, column=3)

   Label(frame, text="Mã thuê phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
   entry_mtp = ttk.Combobox(frame, width=10)
   entry_mtp.grid(row=2, column=1)

   Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=2, column=2)
   entry_mnv = ttk.Combobox(frame, width=10)
   entry_mnv.grid(row=2, column=3)

   Label(frame, text="Tổng tiền:", font=("Times New Roman", 14)).grid(row=3, column=0)
   entry_tot = Label(frame, width=15, font=("Times New Roman"))
   entry_tot.grid(row=3, column=1)

   frame.pack(padx=4, pady=4, anchor="center")

   frame_bang = Frame(rootHD)
   frame_bang.pack(pady=5, expand=True)

   columns = ("Mã hoá đơn", "Mã khách hàng", "Mã thuê phòng", "Mã nhân viên", "Tổng tiền")  # cần dấu phẩy ở cuối
   tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=10)

   # Thanh cuộn
   scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
   scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
   tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

   scroll_y.pack(side="right", fill="y")
   scroll_x.pack(side="bottom", fill="x")
   tree.pack(side="left", expand=True)

   tree.heading("Mã hoá đơn", text="Mã hoá đơn")
   tree.heading("Mã khách hàng", text="Mã khách hàng")
   tree.heading("Mã thuê phòng", text="Mã thuê phòng")
   tree.heading("Mã nhân viên", text="Mã nhân viên")
   tree.heading("Tổng tiền", text="Tổng tiền")

   tree.column("Mã hoá đơn", width=100, anchor="center")
   tree.column("Mã khách hàng", width=100, anchor="center")
   tree.column("Mã thuê phòng", width=100, anchor="center")
   tree.column("Mã nhân viên", width=100, anchor="center")
   tree.column("Tổng tiền", width=100, anchor="center")

   tree.pack(padx=5, pady=10, fill="x")

   def kt_mahd(mahd):
       soma = len(mahd)
       if soma != 6:
           return False
       if mahd[0].isupper() and mahd[1].isupper() and mahd[2].isdigit() and mahd[3].isdigit() and mahd[4].isdigit() and mahd[5].isdigit():
           return True
       else:
           return False


   def load_makh_combobox(): #djgsadqvjudaqhdasjhdvhjs
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

   def load_matp_combobox():
       try:
           cur.execute("select MaTP from ThuePhong")
           matp_data = cur.fetchall()
           matp_list = [row[1] for row in matp_data]
           entry_mtp["values"] = matp_list
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load mã nhân viên{e}")


   def lay_thanhtien_thanh_tongtien():
       try:
           matp = entry_mtp.get()
           cur.execute("select ThanhTien from ThuePhong where MaTP = %s", (matp,))
           matp_data = cur.fetchall()
           if not matp_data:
                messagebox.showwarning("Không tìm thấy mã thuê phòng", "Vui lòng nhập lại thông tin")
                return None
           tongtien = float(matp_data[0])
           return tongtien
       except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi tính tổng tiền{e}")
           return None, None

   def hien_tongtien():
       matp = entry_mtp.get()





