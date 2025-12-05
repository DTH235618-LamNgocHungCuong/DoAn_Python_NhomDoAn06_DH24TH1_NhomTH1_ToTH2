CREATE DATABASE QLKS_DA
ON
(
	NAME = N'QLKS_DA_d',
	FILENAME = N'D:\QLKS\QLKS_DA_data.mdf',
	SIZE = 8MB,
	MAXSIZE = 80MB,
	FILEGROWTH = 2MB
)
LOG ON 
(
	NAME = N'QLKS_DA_lg',
	FILENAME = N'D:\QLKS\QLKS_DA_log.ldf',
	SIZE = 8MB,
	FILEGROWTH = 2MB
);

USE master;
GO

ALTER DATABASE QLKS_DA SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO

DROP DATABASE QLKS_DA;
GO

USE QLKS_DA




CREATE TABLE Phong
(
    MaPh VARCHAR(5) check(MaPh like'[A-Z][A-Z][0-9][0-9][0-9]') NOT NULL,
	LoaiPh NVARCHAR(100) NOT NULL,
    GiaPh NUMERIC(10,3)  DEFAULT 0 check(GiaPh >=0),

    PRIMARY KEY (MaPh),
);
GO




CREATE TABLE KhachHang
(
    MaKH VARCHAR(4) check(MAKH like'[A-Z][0-9][0-9][0-9]') NOT NULL,
    TenKH NVARCHAR (100) NOT NULL UNIQUE,
    DThoaiKH VARCHAR(10) NOT NULL check (DThoaiKH like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DChiKH NVARCHAR(100) NOT NULL,


    PRIMARY KEY (MaKH),
);
GO

CREATE TABLE NhanVien
(
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    TenNV NVARCHAR (100) NOT NULL UNIQUE,
    GioiTinhNV nvarchar (10) NOT NULL check (GioiTinhNV = N'Nam' or GioiTinhNV =  N'Nữ'),
    DThoaiNV VARCHAR(10) NOT NULL check (DThoaiNV like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DChiNV NVARCHAR(100) NOT NULL,
    ChucVu NVARCHAR (100) NOT NULL,
	MatKhau VARCHAR(50) NOT NULL,

    PRIMARY KEY (MaNV),
);
GO


CREATE TABLE ThuePhong
(
    MaTP VARCHAR(6) check(MaTP like'[A-Z][A-Z][0-9][0-9][0-9][0-9]') NOT NULL,
    MaKH VARCHAR(4) check(MaKH like'[A-Z][0-9][0-9][0-9]') NOT NULL,
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    MaPh VARCHAR(5) check(MAPh like'[A-Z][A-Z][0-9][0-9][0-9]')  NOT NULL,
    NgDen DATE NOT NULL, 
    NgDi DATE NOT NULL,
    SoNgay AS (DATEDIFF (day,NgDen,NgDi)) PERSISTED,
    ThanhTien NUMERIC(18,3)  DEFAULT 0 check(ThanhTien >=0) NULL,

    PRIMARY KEY (MaTP),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaPh) REFERENCES Phong(MaPh),
	CONSTRAINT ngden_khac_ngdi check (NgDen < NgDi),
);
GO

CREATE TABLE HoaDon
(
    MaHD VARCHAR(6) check(MAHD like'[A-Z][A-Z][0-9][0-9][0-9][0-9]') NOT NULL,
    MaKH VARCHAR(4) check(MAKH like'[A-Z][0-9][0-9][0-9]') NOT NULL,
    MaTP VARCHAR(6) check(MaTP like'[A-Z][A-Z][0-9][0-9][0-9][0-9]') NOT NULL,
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    TongTien NUMERIC(18,3)  DEFAULT 0 check(TongTien >=0) NULL,

    PRIMARY KEY (MaHD),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaTP) REFERENCES ThuePhong(MaTP),
);
GO



Insert into Phong values ('GG133',N'Giađình', '100.000')
Insert into Phong values ('GI320',N'Đôi', '80.000')
Insert into Phong values ('GN510',N'Đơn', '50.000')
Insert into Phong values ('GI920',N'Đôi', '80.000')

	
Insert into KhachHang values ('D308',N'Trần Quan Chiến', '0999457223',N'Tỉnh An Giang Phường Long_Xuyên')
Insert into KhachHang values ('A195',N'Lê Thị Kim', '0989457330',N'Tỉnh An Giang Phường Long Xuyên')
Insert into KhachHang values ('B208',N'Nguyễn Văn Kiệt', '0973478330',N'Tỉnh An Giang Phường Long_Xuyên')


Insert into NhanVien values ('T8Z23',N'Nguyễn Thanh Kim',N'Nữ','0876235117',N'Tình An Giang Phường Long Xuyên',N'Nhan viên dọn vệ sinh')
Insert into NhanVien values ('T7B52', N'Lê Văn Điền', N'Nam', '0811762357', N'Tình An Giang Phường Long Xuyên',N'Nhân viên dọn vệ sinh')
Insert into NhanVien values ('A1S59', N'Trần Thị Mai', N'Nữ', '0911237656', N'Tình An Giang Phường Long Xuyên',N'Tiếp tân')
Insert into NhanVien values ('A1T43', N'Huỳnh Thị Trúc', N'Nữ', '0919777831', N'Tình An Giang Phường Long Xuyên',N'Tiếp tân')

	
Insert into ThuePhong values ('TT5713', 'A195', 'A1K59', 'GI920', '2025-11-10', '2025-11-20', NULL)
Insert into ThuePhong values ('TQ7783', 'D308', 'A1K59', 'GN510', '2025-10-20', '2025-11-05', NULL)
Insert into ThuePhong values ('TT7873', 'D308', 'A1K59', 'GN510', '2025-12-30', '2026-01-20', NULL)


Insert into HoaDon values ('HT5713', 'A195', 'TT5713', 'A1K59', NULL)
Insert into HoaDon values ('HQ7783', 'D308', 'TQ7783', 'A1K59', NULL)
Insert into HoaDon values ('HT7873', 'D308', 'TT7873', 'A1K59', NULL)



SELECT*FROM Phong
SELECT*FROM KhachHang
SELECT*FROM NhanVien
SELECT*FROM ThuePhong
SELECT*FROM HoaDon
--chọn từ bảng ct thuê phòng
UPDATE ThuePhong
SET ThanhTien = q.DonGia * ThuePhong.SoNgay
FROM 
(
	SELECT 
		p.MaPh,
		p.GiaPh AS DonGia
	FROM Phong p
	) q
WHERE q.MaPh = ThuePhong.MaPh 
	 
UPDATE HoaDon
SET TongTien = tp.ThanhTien
FROM ThuePhong tp
WHERE tp.MaTP = HoaDon.MaTP



