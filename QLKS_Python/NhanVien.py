from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import filedialog, messagebox
from SQL_connec import connect_db, get_all_codes
import pyodbc

entry_mnv = None
entry_tnv = None
rdb_gtnv = None
entry_dtnv = None
entry_dcnv = None
entry_cvnv = None

def open_NhanVien():
    def center_window(win, w=900, h=700):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    rootNV = Tk()
    rootNV.title("Quản lý Nhân Viên")
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
    rdb_gtnv = StringVar(value="Nam")
    Radiobutton(frame, text="Nam", variable=rdb_gtnv, value="Nam").grid(row=2, column=1, sticky="w")
    Radiobutton(frame, text="Nữ", variable=rdb_gtnv, value="Nữ").grid(row=2, column=1, sticky="e")

    Label(frame, text="Điện thoại:", font=("Times New Roman", 14)).grid(row=2, column=2)
    entry_dtnv = Entry(frame, width=15)
    entry_dtnv.grid(row=2, column=3)

    Label(frame, text="Địa chỉ:", font=("Times New Roman", 14)).grid(row=3, column=0)
    entry_dcnv = Entry(frame, width=15)
    entry_dcnv.grid(row=3, column=1)

    Label(frame, text="Chức vụ:", font=("Times New Roman", 14)).grid(row=3, column=2)
    entry_cvnv = Entry(frame, width=15)
    entry_cvnv.grid(row=3, column=3)

    frame.pack(padx=4, pady=4, anchor="center")

    frame_bang = Frame(rootNV)
    frame_bang.pack(pady=5, expand=True)

    # Treeview
    columns = ("Mã_nhân_viên", "Tên_nhân_viên", "Giới_tính", "Điện_thoại", "Địa_chỉ", "Chức_vụ")  # cần dấu phẩy ở cuối
    tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=12)

    # Thanh cuộn
    scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
    scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", expand=True)
   
    tree.heading("Mã_nhân_viên", text="Mã_nhân_viên")
    tree.heading("Tên_nhân_viên", text="Tên_nhân_viên")
    tree.heading("Giới_tính", text="Giới_tính")
    tree.heading("Điện_thoại", text="Điện_thoại")
    tree.heading("Địa_chỉ", text="Địa_chỉ")
    tree.heading("Chức_vụ", text="Chức_vụ")
   
    tree.column("Mã_nhân_viên", width=80, anchor="center")
    tree.column("Tên_nhân_viên", width=200)
    tree.column("Giới_tính", width=80, anchor="center")
    tree.column("Điện_thoại", width=150)
    tree.column("Địa_chỉ", width=200)
    tree.column("Chức_vụ", width=200)
   
    tree.pack(padx=10, pady=5, fill="both")

    def clear_input():
        entry_mnv.config(state='normal')
        entry_mnv.delete(0, END)
        entry_tnv.delete(0, END)
        rdb_gtnv.set("Nam")
        entry_dtnv.delete(0, END)
        entry_dcnv.delete(0, END)
        entry_cvnv.delete(0, END)

    def load_data():
        for i in tree.get_children(): tree.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor()
        try:
           cur.execute("SELECT * FROM NhanVien")
           for row in cur.fetchall():
               tree.insert("", END, values=row)
        except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
        finally:
           if conn: conn.close()

    def them_nhanvien():
        manv = entry_mnv.get().strip()
        tennv = entry_tnv.get()
        gtnv = rdb_gtnv.get()
        dtnv = entry_dtnv.get()
        dcnv = entry_dcnv.get()
        cvnv = entry_cvnv.get()

        if not manv or not tennv or not gtnv or not dtnv or not dcnv or not cvnv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin nhân viên.")
            return
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 

        try:
            # kt xem tang có bị trùng ko
            cur.execute("SELECT COUNT(*) FROM NhanVien where MaNV = ?", (manv,))

            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lập", f"Phòng {manv} đã tồn tại")
                return

            sql = "Insert into NhanVien (MaNV, TenNV, GioiTinhNV, DThoaiNV, DChiNV, ChucVu) VALUES (?, ?, ?, ?, ?, ?)"
            params = (manv, tennv, gtnv, dtnv, dcnv, cvnv)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm nhân viên mới")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"{e}")
        finally:
            if conn: conn.close()   

    def xoa_nhanvien():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
            return  
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa nhân viên?"):
            return
        
        manv = tree.item(selected, "values")[0]
        conn = connect_db()
        if not conn: return
        cur = conn.cursor() 
        try:
            #Kiểm tra ràng buộc khóa ngoại
            cur.execute("SELECT COUNT(*) FROM NhanVien WHERE MaNV = ?", (manv,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Nhân Viên {manv} vì có Thuê Phòng đang tham chiếu.")
                return 

            cur.execute("DELETE FROM NhanVien where MaNV=?", (manv,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xoá")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")
        finally:
            if conn: conn.close()
        load_data()

    def sua_nhanvien():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để sửa")
            return  
        values = tree.item(selected)["values"]
        clear_input()
        entry_mnv.insert(0, values[0]) #khóa
        entry_mnv.config(state='readonly')
        entry_tnv.insert(0, values[1])
        rdb_gtnv.set(values[2])
        entry_dtnv.insert(0, values[3])
        entry_dcnv.insert(0, values[4])
        entry_cvnv.insert(0, values[5])

    def luu_nhanvien():
        manv = entry_mnv.get().strip()
        tennv = entry_tnv.get()
        gtnv = rdb_gtnv.get()
        dtnv = entry_dtnv.get()
        dcnv = entry_dcnv.get()
        cvnv = entry_cvnv.get()

        if not manv or not tennv or not gtnv or not dtnv or not dcnv or not cvnv:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin nhân viên.")
            return
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = "UPDATE NhanVien SET TenNV=?, GioiTinhNV=?, DThoaiNV=?, DChiNV=?, ChucVu=? WHERE MaNV=?"
            params = (tennv, gtnv, dtnv, dcnv, cvnv, manv)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            entry_mnv.config(state='normal')
            messagebox.showinfo("Thành công", "Đã lưu thông tin nhân viên")
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"Lỗi:{e}")
        finally:
            if conn: conn.close()


    
    frame_btn = Frame(rootNV)
    frame_btn.pack(padx=5, pady=10, anchor="center")
       
    Button(frame_btn, text="Thêm", width=8, command=them_nhanvien).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, command=luu_nhanvien).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, command=sua_nhanvien).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=1, column=0, padx=5)
    Button(frame_btn, text="Xoá", width=8, command=xoa_nhanvien).grid(row=1, column=1, padx=5)
    Button(frame_btn, text="Thoát", width=8, command=rootNV.quit).grid(row=0, column=3, padx=5)

   

    load_data()

    rootNV.mainloop()

    