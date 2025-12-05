from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import filedialog, messagebox
from SQL_connec import connect_db, get_all_codes
import pyodbc

entry_mkh = None
entry_tkh = None
entry_dtkh = None
entry_dckh = None

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
    entry_tkh = Entry(frame, width=20)
    entry_tkh.grid(row=1, column=3)

    Label(frame, text="Điện thoại:", font=("Times New Roman", 14)).grid(row=2, column=0)
    entry_dtkh = Entry(frame, width=10)
    entry_dtkh.grid(row=2, column=1)

    Label(frame, text="Địa chỉ:", font=("Times New Roman", 14)).grid(row=2, column=2)
    entry_dckh = Entry(frame, width=30)
    entry_dckh.grid(row=2, column=3)

    frame.pack(padx=4, pady=4, anchor="center")

    frame_bang = Frame(rootKH)
    frame_bang.pack(pady=5, expand=True)

    # Treeview
    columns = ("Mã_khách_hàng", "Tên_khách_hàng", "Điện_thoại", "Địa_chỉ")  # cần dấu phẩy ở cuối
    tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=12)

    # Thanh cuộn
    scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
    scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", expand=True)

    tree.heading("Mã_khách_hàng", text="Mã_khách_hàng")
    tree.heading("Tên_khách_hàng", text="Tên_khách_hàng")
    tree.heading("Điện_thoại", text="Điện_thoại")
    tree.heading("Địa_chỉ", text="Địa_chỉ")

    tree.column("Mã_khách_hàng", width=80, anchor="center")
    tree.column("Tên_khách_hàng", width=150)
    tree.column("Điện_thoại", width=100)
    tree.column("Địa_chỉ", width=250)

    tree.pack(padx=10, pady=5, fill="both")

    def clear_input():
        entry_mkh.config(state='normal')
        entry_mkh.delete(0, END)
        entry_tkh.delete(0, END)
        entry_dtkh.delete(0, END)
        entry_dckh.delete(0, END)

    def load_data():
        for i in tree.get_children(): tree.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor()
        try:
           cur.execute("SELECT * FROM KhachHang")
           for row in cur.fetchall():
               tree.insert("", END, values=list(row))
        except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
        finally:
           if conn: conn.close()

    def them_khachhang():
        makh = entry_mkh.get().strip()
        tenkh = entry_tkh.get()
        dienthoai = entry_dtkh.get()
        diachi = entry_dckh.get()

        if not makh or not tenkh or not dienthoai or not diachi:
            messagebox.showwarning("Chưa nhập", "Hãy nhập đầy đủ thông tin khách hàng")
            return
        
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO KhachHang (MaKH, TenKH, DThoaiKH, DChiKH) VALUES (?, ?, ?, ?)",
                        (makh, tenkh, dienthoai, diachi))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm khách hàng")
            load_data()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"Lỗi: {e}")
        finally:
            if conn: conn.close()

    def xoa_khachhang():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
            return  
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?"):
            return
       
        makh = tree.item(selected, "values")[0]
        conn = connect_db()
        if not conn: return
        cur = conn.cursor()
        try:
            #Kiểm tra ràng buộc khóa ngoại
            cur.execute("SELECT COUNT(*) FROM KhachHang WHERE MaKH = ?", (makh,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Khách Hàng {makh} vì có Thuê Phòng đang tham chiếu.")
                return 

            cur.execute("DELETE FROM KhachHang where MaKH=?", (makh,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xoá khách hàng")
        except Exception as e:
            messagebox.showerror("Lỗi xoá", f"Lỗi: {e}")
        finally:
            if conn: conn.close()
        load_data()

    def sua_khachhang():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để sửa")
            return  
        values = tree.item(selected)["values"]
        clear_input()
        entry_mkh.insert(0, values[0]) #khóa
        entry_mkh.config(state='readonly')
        entry_tkh.insert(0, values[1])
        entry_dtkh.insert(0, values[2])
        entry_dckh.insert(0, values[3])

    def luu_khachhang():
        makh = entry_mkh.get().strip()
        tenkh = entry_tkh.get()
        dienthoai = entry_dtkh.get()
        diachi = entry_dckh.get()

        if not makh or not tenkh or not dienthoai or not diachi:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin khách hàng.")
            return
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor()
        try:
            sql = "UPDATE NhanVien SET TenKH=?, DThoaiKH=?, DChiKH=? WHERE MaKH=?"
            params = (tenkh, dienthoai, diachi, makh)
            cur.execute(sql, params)
            conn.commit()
            
            load_data()
            clear_input()
            entry_mkh.config(state='normal')
            messagebox.showinfo("Thành công", "Đã lưu thông tin khách hàng")
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"Lỗi: {e}")
        finally:
            if conn: conn.close()

    frame_btn = Frame(rootKH)
    frame_btn.pack(padx=5, pady=10, anchor="center")
       
    Button(frame_btn, text="Thêm", width=8, command=them_khachhang).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, command=luu_khachhang).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, command=sua_khachhang).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=1, column=0, padx=5)
    Button(frame_btn, text="Xoá", width=8, command=xoa_khachhang).grid(row=1, column=1, padx=5)
    Button(frame_btn, text="Thoát", width=8, command=rootKH.quit).grid(row=1, column=2, padx=5)

    load_data()

    rootKH.mainloop()

