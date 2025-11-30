CREATE DATABASE QLKS_DA
ON
(
	NAME = N'QLKS_DA_d',
	FILENAME = N'C:\QLKS\QLKS_DA_data.mdf',
	SIZE = 8MB,
	MAXSIZE = 80MB,
	FILEGROWTH = 2MB
)
LOG ON 
(
	NAME = N'QLKS_DA_lg',
	FILENAME = N'C:\QLKS\QLKS_DA_log.ldf',
	SIZE = 8MB,
	FILEGROWTH = 2MB
)




USE master;
GO


ALTER DATABASE QLKS_DA SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
GO


DROP DATABASE QLKS_DA;
GO


USE QLKS_DA


CREATE TABLE Tang
(
    Tang INT check(Tang >= 0 AND Tang <= 20) NOT NULL, 
 
    PRIMARY KEY (Tang),
);
GO


CREATE TABLE LoaiPhong
(
    MaLPh VARCHAR(4) check(MaLPh like '[A-Z][A-Z][A-Z][A-Z]'),
    LoaiPh NVARCHAR(100) NOT NULL UNIQUE,
    GiaPh NUMERIC(10,3)  DEFAULT 0 check(GiaPh >=0) UNIQUE,

    PRIMARY KEY (MaLPh),
);
GO


CREATE TABLE Phong
(
    MaPh VARCHAR(5) check(MaPh like'[A-Z][A-Z][0-9][0-9][0-9]') NOT NULL,
    MaLPh VARCHAR(4) check(MaLPh like '[A-Z][A-Z][A-Z][A-Z]'),
    Tang INT check(Tang >= 0 AND Tang <= 20) NOT NULL, 

    PRIMARY KEY (MaPh),
    FOREIGN KEY (MaLPh) REFERENCES LoaiPhong(MaLPh),
    FOREIGN KEY (Tang) REFERENCES Tang(Tang),
);
GO




CREATE TABLE KhachHang
(
    MaKH VARCHAR(4) check(MAKH like'[A-Z][0-9][0-9][0-9]') NOT NULL,
    TenKH NVARCHAR (100) NOT NULL UNIQUE,
    GioiTinhKH nvarchar (10) NOT NULL check (GioiTinhKH = N'Nam' or GioiTinhKH =  N'Nữ'),
    DThoaiKH VARCHAR(10) NOT NULL check (DThoaiKH like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DChiKH NVARCHAR(100) NOT NULL,


    PRIMARY KEY (MaKH),
);
GO


CREATE TABLE ChucVu
(
    MaCV VARCHAR(4) check(MACV like'[A-Z][A-Z][A-Z]') NOT NULL,
    TenCV NVARCHAR (100) NOT NULL UNIQUE,


    PRIMARY KEY (MaCV),
);
GO


CREATE TABLE NhanVien
(
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    TenNV NVARCHAR (100) NOT NULL UNIQUE,
    GioiTinhNV nvarchar (10) NOT NULL check (GioiTinhNV = N'Nam' or GioiTinhNV =  N'Nữ'),
    DThoaiNV VARCHAR(10) NOT NULL check (DThoaiNV like '[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    DChiNV NVARCHAR(100) NOT NULL,
    MaCV VARCHAR(4) check(MACV like'[A-Z][A-Z][A-Z]') NOT NULL,
    TangTruc INT check(TangTruc >= 0 AND TangTruc <= 20) NOT NULL,
	MatKhau VARCHAR(50) NOT NULL,

    PRIMARY KEY (MaNV),
    FOREIGN KEY (MaCV) REFERENCES ChucVu(MaCV),
    FOREIGN KEY (TangTruc) REFERENCES Tang(Tang),


);
GO


CREATE TABLE ThuePhong
(
    MaTP VARCHAR(6) check(MAHD like'[A-Z][A-Z][0-9][0-9][0-9][0-9]') NOT NULL,
    MaKH VARCHAR(4) check(MAKH like'[A-Z][0-9][0-9][0-9]') NOT NULL,
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    MaPh VARCHAR(5) check(MAPh like'[A-Z][A-Z][0-9][0-9][0-9]')  NOT NULL,
    NgDen DATE NOT NULL, 
    NgDi DATE NOT NULL,
    SoNgay AS (DATEDIFF (day,NgDen,NgDi)) PERSISTED,
    ThanhTien NUMERIC(18,3)  DEFAULT 0 check(TongTien >=0) NULL,

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
    MaTP VARCHAR(6) check(MAHD like'[A-Z][A-Z][0-9][0-9][0-9][0-9]') NOT NULL,
    MaNV VARCHAR(5) check(MaNV like'[A-Z][0-9][A-Z][0-9][0-9]')  NOT NULL,
    TongTien NUMERIC(18,3)  DEFAULT 0 check(TongTien >=0) NULL,


    PRIMARY KEY (MaHD),
    FOREIGN KEY (MaKH) REFERENCES KhachHang(MaKH),
    FOREIGN KEY (MaNV) REFERENCES NhanVien(MaNV),
    FOREIGN KEY (MaTP) REFERENCES ThuePhong(MaTP),
);
GO

Insert into Tang values ('0')
Insert into Tang values ('1')
Insert into Tang values ('2')
Insert into Tang values ('3')
Insert into Tang values ('4')
Insert into Tang values ('5')
Insert into Tang values ('6')
Insert into Tang values ('7')
Insert into Tang values ('8')
Insert into Tang values ('9')




Insert into LoaiPhong values ('GDON',N'Giường Đơn', '50.000')
Insert into LoaiPhong values ('GDOI',N'Giường Đôi', '80.000')
Insert into LoaiPhong values ('PGID',N'Phòng gia đình', '100.000')




Insert into Phong values ('GG133','PGID','1')
Insert into Phong values ('GI320','GDOI','3')
Insert into Phong values ('GN510','GDON','5')
Insert into Phong values ('GI920','GDOI','9')




Insert into KhachHang values ('D308',N'Trần Quan Chiến', N'Nam', '0999457223',N'Tình An Giang, Phường Long Xuyên')
Insert into KhachHang values ('A195',N'Lê Thị Kim', N'Nữ', '0989457330',N'Tình An Giang, Phường Long Xuyên')




Insert into ChucVu values ('DVS',N'Dọn vệ sinh')
Insert into ChucVu values ('QTT',N'Tiếp tân')




Insert into NhanVien values ('T8Z23', N'Nguyễn Thanh Kim', N'Nữ', '0876235117', N'Tình An Giang, Phường Long Xuyên', 'DVS', '8', 'KL3017')
Insert into NhanVien values ('T7B52', N'Lê Văn Điền', N'Nam', '0811762357', N'Tình An Giang, Phường Long Xuyên', 'DVS', '7', '93433624')
Insert into NhanVien values ('A1K59', N'Trần Thị Mai', N'Nữ', '0911237656', N'Tình An Giang, Phường Long Xuyên', 'QTT', '0', 'KPYFTYTG')


Insert into ThuePhong values ('TT5713', 'A195', 'A1K59', 'GI920', '2025-11-10', '2025-11-20', NULL)
Insert into ThuePhong values ('TQ7783', 'D308', 'A1K59', 'GN510', '2025-10-20', '2025-11-05', NULL)
Insert into ThuePhong values ('TT7873', 'D308', 'A1K59', ‘GN510', '2025-12-30', '2026-01-20', NULL)


Insert into HoaDon values ('HT5713', 'A195', 'TT5713', 'A1K59', NULL)
Insert into HoaDon values ('HQ7783', 'D308', 'TQ7783', 'A1K59', NULL)
Insert into HoaDon values ('HT7873', 'D308', 'TT7873', 'A1K59', NULL)



SELECT*FROM Tang
SELECT*FROM LoaiPhong
SELECT*FROM Phong
SELECT*FROM KhachHang
SELECT*FROM ChucVu
SELECT*FROM NhanVien


--SELECT*FROM LoaiPhong
--SELECT*FROM Phong
SELECT*FROM ThuePhong
SELECT*FROM HoaDon
--chọn từ bảng ct thuê phòng
UPDATE ThuePhong
SET ThanhTien = q.DonGia * ThuePhong.SoNgay
FROM 
(
	SELECT 
		p.MaLPh,
		p.MaPh,
		lp2.GiaPh AS DonGia
	FROM LoaiPhong lp2, Phong p
	where lp2.MaLPh = p.MaLPh
	) q
WHERE q.MaPh = ThuePhong.MaPh 
	
– 
UPDATE HoaDon
SET TongTien = tp.ThanhTien
FROM ThuePhong tp
WHERE tp.MaTP = HoaDon.MaTP






