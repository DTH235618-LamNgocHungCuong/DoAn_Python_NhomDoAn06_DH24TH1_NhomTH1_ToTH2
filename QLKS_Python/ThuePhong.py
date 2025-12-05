from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import filedialog, messagebox
from decimal import Decimal
import pyodbc

from SQL_connec import connect_db, get_all_codes

entry_mtp = None
cbb_mkh = None
cbb_mnv = None
cbb_mp = None
date_entry_nd = None
date_entry_ndi = None
entry_songay = None
entry_thanhtien = None

def refresh_ma_ngoai_comboboxes():
    global cbb_mkh, cbb_mnv, cbb_mp
    #chỉ cập nhật được khi combobox đã được tạo
    if cbb_mkh is not None:
        cbb_mkh['values'] = get_all_codes("KhachHang", "MaKH")
    if cbb_mnv is not None:
        cbb_mnv['values'] = get_all_codes("NhanVien", "MaNV")
    if cbb_mp is not None:
        cbb_mp['values'] = get_all_codes("Phong", "MaPh")

def open_ThuePhong():
    def center_window(win, w=900, h=700):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    rootTP = Tk()
    rootTP.title("Quản lý Thuê Phòng")
    rootTP.minsize(900, 700)
    center_window(rootTP)

    Label(rootTP, text="QUẢN LÝ THUÊ PHÒNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

    frame = Frame(rootTP)

    Label(frame, text="Mã thuê phòng:", font=("Times New Roman", 14)).grid(row=1, column=0)
    entry_mtp = Entry(frame, width=10)
    entry_mtp.grid(row=1, column=1)

    Label(frame, text="Mã khách hàng:", font=("Times New Roman", 14)).grid(row=1, column=2)
    cbb_mkh = ttk.Combobox(frame, width=13)
    cbb_mkh['values'] = get_all_codes("KhachHang", "MaKH")
    cbb_mkh.grid(row=1, column=3)

    Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=2, column=0)
    cbb_mnv = ttk.Combobox(frame, width=13)
    cbb_mnv['values'] = get_all_codes("NhanVien", "MaNV")
    cbb_mnv.grid(row=2, column=1)

    Label(frame, text="Mã phòng:", font=("Times New Roman", 14)).grid(row=2, column=2)
    cbb_mp = ttk.Combobox(frame, width=13)
    cbb_mp['values'] = get_all_codes("Phong", "MaPh")
    cbb_mp.grid(row=2, column=3)

    Label(frame, text="Ngày đến:", font=("Times New Roman", 14)).grid(row=3, column=0)
    date_entry_nd = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry_nd.grid(row=3, column=1)

    Label(frame, text="Ngày đi:", font=("Times New Roman", 14)).grid(row=4, column=0)
    date_entry_ndi = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry_ndi.grid(row=4, column=1)

    Label(frame, text="Số ngày:", font=("Times New Roman", 14)).grid(row=3, column=2)
    entry_songay = Entry(frame, width=10, state='readonly')
    entry_songay.grid(row=3, column=3)

    Label(frame, text="Thành tiền:", font=("Times New Roman", 14)).grid(row=4, column=2)
    entry_thanhtien = Entry(frame, width=15, state='readonly')
    entry_thanhtien.grid(row=4, column=3)

    date_entry_nd.bind("<<DateEntrySelected>>", lambda e: tinh_songay_va_thanhtien())
    date_entry_ndi.bind("<<DateEntrySelected>>", lambda e: tinh_songay_va_thanhtien())
    cbb_mp.bind("<<ComboboxSelected>>", lambda e: tinh_songay_va_thanhtien())

    frame.pack(padx=4, pady=4, anchor="center")

    frame_bang = Frame(rootTP)
    frame_bang.pack(pady=5, expand=True)

    # Treeview
    columns = ("Mã_thuê_phòng", "Mã_khách_hàng", "Mã_nhân_viên", "Mã_phòng", "Ngày_đến", "Ngày_đi", "Số_ngày", "Thành_tiền")  # cần dấu phẩy ở cuối
    tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=12)

    # Thanh cuộn
    scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
    scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", expand=True)

    tree.heading("Mã_thuê_phòng", text="Mã_thuê_phòng")
    tree.heading("Mã_khách_hàng", text="Mã_khách_hàng")
    tree.heading("Mã_nhân_viên", text="Mã_nhân_viên")
    tree.heading("Mã_phòng", text="Mã_phòng")
    tree.heading("Ngày_đến", text="Ngày_đến")
    tree.heading("Ngày_đi", text="Ngày_đi")
    tree.heading("Số_ngày", text="Số_ngày")
    tree.heading("Thành_tiền", text="Thành_tiền")

    tree.column("Mã_thuê_phòng", width=80, anchor="center")
    tree.column("Mã_khách_hàng", width=100, anchor="center")
    tree.column("Mã_nhân_viên", width=100, anchor="center")
    tree.column("Mã_phòng", width=100, anchor="center")
    tree.column("Ngày_đến", width=90, anchor="center")
    tree.column("Ngày_đi", width=90, anchor="center")
    tree.column("Số_ngày", width=60, anchor="center")
    tree.column("Thành_tiền", width=100)

    tree.pack(padx=10, pady=5, fill="both")

    def tinh_songay_va_thanhtien():
        try:
            nd_val = date_entry_nd.get()
            ndi_val = date_entry_ndi.get()
            mp_val = cbb_mp.get()
            if not nd_val or not ndi_val or not mp_val:
                return #thiếu dữ liệu thì không làm gì cả

            nd = datetime.strptime(date_entry_nd.get(), '%Y-%m-%d')
            ndi = datetime.strptime(date_entry_ndi.get(), '%Y-%m-%d')
            if ndi <= nd:
                messagebox.showwarning("Lỗi ngày", "Ngày đi phải sau ngày đến.")
                return
            songay = (ndi - nd).days
            entry_songay.config(state='normal')
            entry_songay.delete(0, END)
            entry_songay.insert(0, str(songay))
            entry_songay.config(state='readonly')

            # Giả sử lấy giá phòng từ cơ sở dữ liệu
            conn = connect_db()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT GiaPh FROM Phong WHERE MaPh = ?", (cbb_mp.get(),))
            result = cur.fetchone()
            if result:
                giaphong = result[0]
                thanhtien = songay * float(giaphong)

                thanhtien_str = f"{thanhtien:.3f}"
                
                entry_thanhtien.config(state='normal')
                entry_thanhtien.delete(0, END)
                entry_thanhtien.insert(0, thanhtien_str)
                entry_thanhtien.config(state='readonly')
            if conn: conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi tính toán", f"Lỗi: {e}")

    def clear_input():
        entry_mtp.config(state='normal')
        entry_mtp.delete(0, END)
        cbb_mkh.set("")
        cbb_mnv.set("")
        cbb_mp.set("")
        date_entry_nd.set_date(date.today().strftime('%Y-%m-%d'))
        date_entry_ndi.set_date(date.today().strftime('%Y-%m-%d'))
        entry_songay.config(state='normal')
        entry_songay.delete(0, END)
        entry_songay.config(state='readonly')
        entry_thanhtien.config(state='normal')
        entry_thanhtien.delete(0, END)
        entry_thanhtien.config(state='readonly')

    def load_data():
        for i in tree.get_children(): tree.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor()
        try:
           cur.execute("SELECT * FROM ThuePhong")
           for row in cur.fetchall():
               display_row = list(row)
               display_row[4] = display_row[4].strftime('%Y-%m-%d')
               display_row[5] = display_row[5].strftime('%Y-%m-%d')

               if isinstance (display_row[7], Decimal):
                   display_row[7] = f"{display_row[7]:.3f}"
               else:
                   display_row[7] = f"{float(display_row[7]):.3f}"

               tree.insert("", END, values=tuple(display_row))
        except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
        finally:
           if conn: conn.close()

    
    def them_thuephong():
        matp = entry_mtp.get().strip()
        makh = cbb_mkh.get().strip()
        manv = cbb_mnv.get().strip()
        maph = cbb_mp.get().strip()
        ngayden = date_entry_nd.get()
        ngaydi = date_entry_ndi.get()

        try:
            songay = int(entry_songay.get().strip())
            thanhtien = float(entry_thanhtien.get().strip())
        except ValueError:
            messagebox.showwarning("Lỗi dữ liệu", "Số ngày hoặc Thành tiền không hợp lệ.")
            return

        if not matp or not makh or not manv or not maph or not ngayden or not ngaydi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin thuê phòng.")
            return  

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 

        try:
            # kt xem tang có bị trùng ko
            cur.execute("SELECT COUNT(*) FROM ThuePhong where MaTP = ?", (matp,))

            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lập", f"Mã Thuê Phòng {matp} đã tồn tại")
                return

            sql = "Insert into ThuePhong (MaTP, MaKH, MaNV, MaPh, NgDen, NgDi) VALUES (?, ?, ?, ?, ?, ?)"
            params = (matp, makh, manv, maph, ngayden, ngaydi)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm phòng mới")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"{e}")
        finally:
            if conn: conn.close()

    def xoa_thuephong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
            return  
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thuê phòng?"):
            return
       
        matp = tree.item(selected, "values")[0]
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM ThuePhong WHERE MaTP = ?", (matp,))
            conn.commit()
            messagebox.showinfo("Thành công", f"Đã xóa thuê phòng {matp}")
            load_data()
        except Exception as e:
            messagebox.showerror("Lỗi xoá", f"Lỗi: {e}")
        finally:
            if conn: conn.close()
        load_data

    def sua_thuephong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để sửa")
            return  
        values = tree.item(selected)["values"]
        clear_input()

        entry_mtp.insert(0, values[0]) #khóa
        entry_mtp.config(state='readonly')
        cbb_mkh.set(values[1])
        cbb_mnv.set(values[2])
        cbb_mp.set(values[3])
        if values[4]: date_entry_nd.set_date(values[4])
        if values[5]: date_entry_ndi.set_date(values[5])

    def luu_thuephong():
        matp = entry_mtp.get().strip()
        makh = cbb_mkh.get().strip()
        manv = cbb_mnv.get().strip()
        maph = cbb_mp.get().strip()
        ngayden = date_entry_nd.get()
        ngaydi = date_entry_ndi.get()

        try:
            songay = int(entry_songay.get().strip())
            thanhtien = float(entry_thanhtien.get().strip())
        except ValueError:
            messagebox.showwarning("Lỗi dữ liệu", "Số ngày hoặc Thành tiền không hợp lệ.")
            return

        if not matp or not makh or not manv or not maph or not ngayden or not ngaydi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin thuê phòng.")
            return

        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = "UPDATE ThuePhong SET MaKH=?, MaNV=?, MaPh=?, NgDen=?, NgDi=? WHERE MaTP=?"
            params = (makh, manv, maph, ngayden, ngaydi, matp)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            entry_mtp.config(state='normal')
            messagebox.showinfo("Thành công", "Đã lưu thông tin phòng")
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"{e}")
        finally:
            if conn: conn.close()

    tinh_songay_va_thanhtien()

    frame_btn = Frame(rootTP)
    frame_btn.pack(padx=5, pady=10, anchor="center")
       
    Button(frame_btn, text="Thêm", width=8, command=them_thuephong).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, command=luu_thuephong).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, command=sua_thuephong).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=1, column=0, padx=5)
    Button(frame_btn, text="Xoá", width=8, command=xoa_thuephong).grid(row=1, column=1, padx=5)
    Button(frame_btn, text="Thoát", width=8, command=rootTP.destroy).grid(row=0, column=3, padx=5)
    
    load_data()


    rootTP.mainloop()
