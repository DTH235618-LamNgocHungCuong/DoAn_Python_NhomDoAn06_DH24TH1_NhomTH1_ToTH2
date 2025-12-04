from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
#from tkcalendar import DateEntry
from datetime import datetime, date
from tkinter import filedialog, messagebox
from SQL_connec import connect_db, get_all_codes
from decimal import Decimal
import pyodbc


entry_mp = None
entry_lp = None
entry_gp = None
tree = None


def open_Phong():
    def center_window(win, w=800, h=600):
        ws = win.winfo_screenwidth()
        hs = win.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        win.geometry(f'{w}x{h}+{x}+{y}')

    rootP = Tk()
    rootP.title("Quản lý Phòng")
    rootP.minsize(800, 600)
    center_window(rootP)

    Label(rootP, text="QUẢN LÝ PHÒNG", font=("Times New Roman", 18, "bold")).pack(pady=5)

    frame = Frame(rootP)

    Label(frame, text="Mã phòng:", font=("Times New Roman", 14)).grid(row=1, column=0)
    entry_mp = Entry(frame, width=10)
    entry_mp.grid(row=1, column=1)

    Label(frame, text="Loại phòng:", font=("Times New Roman", 14)).grid(row=1, column=2)
    entry_lp = ttk.Combobox(frame, width=10, values=["Đơn", "Đôi", "Giađình"])
    entry_lp.grid(row=1, column=3)

    Label(frame, text="Giá phòng:", font=("Times New Roman", 14)).grid(row=2, column=0)
    entry_gp = Entry(frame, width=10)
    entry_gp.grid(row=2, column=1)

    frame.pack(padx=4, pady=4, anchor="center")

    frame_bang = Frame(rootP)
    frame_bang.pack(pady=5, expand=True)

    # Treeview
    columns = ("Mã_phòng", "Loại_phòng", "Giá_phòng")  # cần dấu phẩy ở cuối
    tree = ttk.Treeview(frame_bang, columns=columns, show="headings", height=12)

    # Thanh cuộn
    scroll_y = Scrollbar(frame_bang, orient="vertical", command=tree.yview)
    scroll_x = Scrollbar(frame_bang, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.pack(side="right", fill="y")
    scroll_x.pack(side="bottom", fill="x")
    tree.pack(side="left", expand=True)
   
    tree.heading("Mã_phòng", text="Mã_phòng")
    tree.heading("Loại_phòng", text="Loại_phòng")
    tree.heading("Giá_phòng", text="Giá_phòng")
   
    tree.column("Mã_phòng", width=80, anchor="center")
    tree.column("Loại_phòng", width=150)
    tree.column("Giá_phòng", width=150, anchor="center")
   
    tree.pack(padx=10, pady=5, fill="both")

    def clear_input():
        entry_mp.config(state='normal')
        entry_mp.delete(0, END)
        entry_lp.set("")
        entry_gp.delete(0, END)

    def load_data():
        for i in tree.get_children(): tree.delete(i) 
        conn = connect_db() 
        if not conn: return 
        cur = conn.cursor()
        try:
           cur.execute("SELECT MaPh, LoaiPh, GiaPh FROM Phong")
           for row in cur.fetchall():
               maph, loaiphong, giaphong = row
               
                # Nếu giá phòng là Decimal ⇒ chuyển thành số thường hoặc chuỗi
               if isinstance(giaphong, Decimal):
                   giaphong = f"{giaphong:.3f}"

               tree.insert("", END, values=(maph, loaiphong, giaphong))
        except Exception as e:
           messagebox.showerror("Lỗi", f"Lỗi load dữ liệu{e}")
        finally:
           if conn: conn.close()

    def them_phong():
        maph = entry_mp.get().strip()
        loaiphong = entry_lp.get()
        giaphong = entry_gp.get()

        if not maph or not loaiphong or not giaphong:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin phòng.")
            return
       
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 

        try:
            # kt xem tang có bị trùng ko
            cur.execute("SELECT COUNT(*) FROM Phong where MaPh = ?", (maph,))

            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Trùng lập", f"Phòng {maph} đã tồn tại")
                return

            sql = "Insert into Phong (MaPh, LoaiPh, GiaPh) VALUES (?, ?, ?)"
            params = (maph, loaiphong, giaphong)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            messagebox.showinfo("Thành công", "Đã thêm phòng mới")
        except Exception as e:
            messagebox.showerror("Lỗi thêm", f"{e}")
        finally:
            if conn: conn.close()

    def xoa_phong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chon", "Hãy chọn 1 dòng để xoá")
            return  
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa phòng?"):
            return
       
        maph = tree.item(selected, "values")[0]
        conn = connect_db()
        if not conn: return
        cur = conn.cursor() 
        try:
            #Kiểm tra ràng buộc khóa ngoại
            cur.execute("SELECT COUNT(*) FROM Phong WHERE MaPh = ?", (maph,))
            if cur.fetchone()[0] > 0:
                messagebox.showwarning("Cảnh báo", f"Không thể xóa Phong {maph} vì có Thuê Phòng đang tham chiếu.")
                return 

            cur.execute("DELETE FROM Phong where MaPh=?", (maph,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xoá")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Lỗi khi xoá:\n{e}")
        finally:
            if conn: conn.close()
        load_data()

    def sua_phong():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn loại phòng để sửa")
            return
        values = tree.item(selected)["values"]
        clear_input()
        entry_mp.insert(0, values[0]) #khóa
        entry_mp.config(state='readonly')
        entry_lp.set(values[1])
        entry_gp.insert(0, values[2])

    def luu_phong():
        maph = entry_mp.get().strip()
        loaiphong = entry_lp.get()
        giaphong = entry_gp.get()

        if not maph or not loaiphong or not giaphong:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ thông tin phòng.")
            return
        
        conn = connect_db() 
        if not conn: return
        cur = conn.cursor() 
        try:
            sql = "UPDATE Phong SET LoaiPh=?, GiaPh=? WHERE MaPh=?"
            params = (loaiphong, giaphong, maph)
            cur.execute(sql, params)
            conn.commit()
            load_data()
            clear_input()
            entry_mp.config(state='normal')
            messagebox.showinfo("Thành công", "Đã lưu thông tin phòng")
        except Exception as e:
            messagebox.showerror("Lỗi lưu", f"{e}")
        finally:
            if conn: conn.close()

    frame_btn = Frame(rootP)
    frame_btn.pack(padx=5, pady=10, anchor="center")
       
    Button(frame_btn, text="Thêm", width=8, command=them_phong).grid(row=0, column=0, padx=5)
    Button(frame_btn, text="Lưu", width=8, command=luu_phong).grid(row=0, column=1, padx=5)
    Button(frame_btn, text="Sửa", width=8, command=sua_phong).grid(row=0, column=2, padx=5)
    Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=1, column=0, padx=5)
    Button(frame_btn, text="Xoá", width=8, command=xoa_phong).grid(row=1, column=1, padx=5)
    Button(frame_btn, text="Thoát", width=8, command=rootP.quit).grid(row=1, column=2, padx=5)

    load_data()

    rootP.mainloop()