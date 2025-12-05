from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import filedialog, messagebox
from SQL_connec import connect_db, get_all_codes
from decimal import Decimal
import pyodbc

entry_mhd = None
cbb_mnv = None
cbb_mtp = None
entry_mkh = None
entry_tongtien = None

def refresh_ma_ngoai_comboboxes():
    global cbb_mtp, cbb_mnv
    #chỉ cập nhật được khi combobox đã được tạo
    if cbb_mnv is not None:
        cbb_mnv['values'] = get_all_codes("NhanVien", "MaNV")
    if cbb_mtp is not None:
        cbb_mtp['values'] = get_all_codes("ThuePhong", "MaTP")

def open_HoaDon():
    def center_window(win, w=900, h=700):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    rootHD = Tk()
    rootHD.title("Quản lý Hóa Đơn")
    rootHD.minsize(900, 700)
    center_window(rootHD)

    Label(rootHD, text="QUẢN LÝ HÓA ĐƠN", font=("Times New Roman", 18, "bold")).pack(pady=5)

    frame = Frame(rootHD)

    Label(frame, text="Mã hóa đơn:", font=("Times New Roman", 14)).grid(row=1, column=0)
    entry_mhd = Entry(frame, width=13)
    entry_mhd.grid(row=1, column=1)

    Label(frame, text="Mã nhân viên:", font=("Times New Roman", 14)).grid(row=1, column=2)
    cbb_mnv = ttk.Combobox(frame, width=13)
    cbb_mnv['values'] = get_all_codes("NhanVien", "MaNV")
    cbb_mnv.grid(row=1, column=3)

    Label(frame, text="Mã thuê phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
    cbb_mtp = ttk.Combobox(frame, width=13)
    cbb_mtp['values'] = get_all_codes("ThuePhong", "MaTP")
    cbb_mtp.grid(row=2, column=1)

    Label(frame, text="Mã khách hàng:", font=("Times New Roman", 14)).grid(row=2, column=2)
    entry_mkh = Entry(frame, width=15, state='readonly')
    entry_mkh.grid(row=2, column=3)

    Label(frame, text="Tổng tiền:", font=("Times New Roman", 14)).grid(row=3, column=0)
    entry_tongtien = Entry(frame, width=15, state='readonly')
    entry_tongtien.grid(row=3, column=1)

    #blind
    cbb_mtp.bind("<<ComboboxSelected>>", lambda e: lay_khachhang_tongtien())

    frame.pack(padx=4, pady=4, anchor="center")

    frame_bang = Frame(rootHD)
    frame_bang.pack(pady=5, expand=True)

    
    columns = ("Mã_hóa_đơn", "Mã-khách_hàng", "Mã_thuê_phòng", "Mã_nhân_viên", "Tổng_tiền")  # cần dấu phẩy ở cuối

    # Treeview
    tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=12)

    # Thanh cuộn
    scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
    scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", expand=True)

    tree.heading("Mã_hóa_đơn", text="Mã_hóa_đơn")
    tree.heading("Mã-khách_hàng", text="Mã-khách_hàng")
    tree.heading("Mã_thuê_phòng", text="Mã_thuê_phòng")
    tree.heading("Mã_nhân_viên", text="Mã_nhân_viên")
    tree.heading("Tổng_tiền", text="Tổng_tiền")

    tree.column("Mã_hóa_đơn", width=80, anchor="center")
    tree.column("Mã-khách_hàng", width=100, anchor="center")  
    tree.column("Mã_thuê_phòng", width=100, anchor="center")
    tree.column("Mã_nhân_viên", width=100, anchor="center")
    tree.column("Tổng_tiền", width=100)

    tree.pack(padx=10, pady=5, fill="both")

    def lay_khachhang_tongtien():
        conn = None
        try:
            matp = cbb_mtp.get().strip()
            if not matp:
                return

            conn = connect_db()
            if not conn: return
            cur = conn.cursor()
            cur.execute("SELECT MaKH, ThanhTien FROM ThuePhong WHERE MaTP = ?", (matp,))
            result = cur.fetchone()
            if result:
                makh = result[0]
                tongtien = result[1]
                entry_mkh.config(state='normal')
                entry_mkh.delete(0, END)
                entry_mkh.insert(0, makh)
                entry_mkh.config(state='readonly')

                entry_tongtien.config(state='normal')
                entry_tongtien.delete(0, END)

                if isinstance(tongtien, Decimal):
                    tongtien_str = f"{tongtien:.3f}"
                else:
                    tongtien_str = f"{float(tongtien):.3f}"

                entry_tongtien.insert(0, str(tongtien))
                entry_tongtien.config(state='readonly')
            else:
                messagebox.showwarning("Lỗi", "Không có thông tin cho Mã thuê phòng này.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi lấy mã khách hàng và tổng tiền: {e}")
        finally:
            if conn: conn.close()



    def clear_input():
        entry_mhd.config(state='normal')
        entry_mhd.delete(0, END)
        cbb_mnv.set("")
        cbb_mtp.set("")
        entry_mkh.config(state='normal')
        entry_mkh.delete(0, END)
        entry_mkh.config(state='readonly')
        entry_tongtien.config(state='normal')
        entry_tongtien.delete(0, END)
        entry_tongtien.config(state='readonly')

    def load_data():
        for i in tree.get_children(): tree.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor()
        try:
           cur.execute("SELECT * FROM HoaDon")
           for row in cur.fetchall():
                row = list(row)

                #row[4] là tổng tiền
                if isinstance(row[4], Decimal):
                    row[4] = f"{row[4]:.3f}"
                else:
                    row[4] = f"{float(row[4]):.3f}"
 
                tree.insert("", END, values=row)
        except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
        finally:
           if conn: conn.close()

    def them_hoadon():
        mahd = entry_mhd.get().strip()
        manv = cbb_mnv.get().strip()
        matp = cbb_mtp.get().strip()

        try:
            makh = entry_mkh.get().strip()
            tongtien = float(entry_tongtien.get().strip())
        except ValueError:
            messagebox.showwarning("Lỗi", "Mã khách hàng và Tổng tiền không hợp lệ.")
            return

        if not mahd or not manv or not matp:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin hóa đơn.")
            return

        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            # Chèn dữ liệu vào bảng HoaDon
            cur.execute("""
                INSERT INTO HoaDon (MaHD, MaKH, MaTP, MaNV)
                VALUES (?, ?, ?, ?)
            """, (mahd, makh, matp, manv))
            conn.commit()
            load_data()
            clear_input()
            entry_mhd.config(state='normal')
            messagebox.showinfo("Thành công", "Đã thêm hóa đơn thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"Lỗi: {e}")
        finally:
            if conn: conn.close()

    def xoa_hoadon():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
            return  
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa hóa đơn?"):
            return
       
        mahd = tree.item(selected, "values")[0]
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM HoaDon WHERE MaHD = ?", (mahd,))
            conn.commit()
            clear_input()
            messagebox.showinfo("Thành công", "Đã xóa hóa đơn")
        except Exception as e:
            messagebox.showerror("Lỗi xoá", f"Lỗi: {e}")
        finally:
            if conn: conn.close()
        load_data()

    def sua_hoadon():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để sửa")
            return  
        values = tree.item(selected)["values"]
        clear_input()
        entry_mhd.insert(0, values[0]) #khóa
        entry_mhd.config(state='readonly')
        cbb_mnv.set(values[1])
        cbb_mtp.set(values[2])

    def luu_hoadon():
        mahd = entry_mhd.get().strip()
        manv = cbb_mnv.get().strip()
        matp = cbb_mtp.get().strip()

        try:
            makh = entry_mkh.get().strip()
            tongtien = float(entry_tongtien.get().strip())
        except ValueError:
            messagebox.showwarning("Lỗi", "Mã khách hàng và Tổng tiền không hợp lệ.")
            return

        if not mahd or not manv or not matp:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng điền đầy đủ thông tin hóa đơn.")
            return

        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:

            # Cập nhật dữ liệu vào bảng HoaDon
            cur.execute("""
                UPDATE HoaDon
                SET MaKH = ?, MaTP = ?, MaNV = ?
                WHERE MaHD = ?
            """, (makh, matp, manv, mahd))
            conn.commit()
            load_data()
            clear_input()
            entry_mhd.config(state='normal')
            messagebox.showinfo("Thành công", "Đã lưu thông tin hóa đơn")
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"Lỗi: {e}")
        finally:
            if conn: conn.close()


    lay_khachhang_tongtien()

    frame_btn = Frame(rootHD)
    frame_btn.pack(padx=5, pady=10, anchor="center")
       
    Button(frame_btn, text="Thêm", width=8, command=them_hoadon).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, command=luu_hoadon).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, command=sua_hoadon).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=1, column=0, padx=5)
    Button(frame_btn, text="Xoá", width=8, command=xoa_hoadon).grid(row=1, column=1, padx=5)
    Button(frame_btn, text="Thoát", width=8, command=rootHD.destroy).grid(row=0, column=3, padx=5)
    
    load_data()
    
    rootHD.mainloop()

