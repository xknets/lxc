USE [master]
GO


CREATE DATABASE library 
ON  PRIMARY 
( NAME = N'library', FILENAME = N'D:\DATA\library.mdf' , SIZE = 2304KB , MAXSIZE = UNLIMITED, FILEGROWTH = 1024KB )
 LOG ON 
( NAME = N'library_log', FILENAME = N'D:\DATA\library_log.LDF' , SIZE = 576KB , MAXSIZE = 2048GB , FILEGROWTH = 10%)
GO


USE library
GO

CREATE TABLE [admins](
	[id] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[password] [nvarchar](20) NULL
)

GO
CREATE TABLE [Users](
	[id] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [nvarchar](100) NOT NULL,
	[tel] [nvarchar](20) NULL
)

GO


CREATE TABLE [Authors](
	[id] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [nvarchar](100) NOT NULL,
) 

GO


CREATE TABLE [Categories](
	[id] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[name] [nvarchar](100) NOT NULL)

GO


CREATE TABLE [Books](
	[ISBN] char(13) PRIMARY KEY NOT NULL,
	[title] [nvarchar](255) NOT NULL,
	[author_id] [int] NULL,
	[category_id] [int] NULL,
	[status] [nvarchar](50) CHECK([status]= '�ɽ�' OR [status] = '�ѽ��') NOT NULL,

) 

GO

ALTER TABLE [Books]  WITH CHECK ADD FOREIGN KEY([author_id])
REFERENCES [Authors] ([id])
GO

ALTER TABLE [Books]  WITH CHECK ADD FOREIGN KEY([category_id])
REFERENCES [Categories] ([id])
GO

ALTER TABLE [Books] ADD  DEFAULT ('�ɽ�') FOR [status]
GO


CREATE TABLE [BorrowRecords](
	[id] [int] IDENTITY(1,1) PRIMARY KEY NOT NULL,
	[book_isbn] char(13)  NULL,
	[user_id] [int] NULL,
	[borrow_date] [datetime] NOT NULL,
	[return_date] [datetime] NULL,
) 

GO

ALTER TABLE [BorrowRecords]  WITH CHECK ADD FOREIGN KEY([book_isbn])
REFERENCES [Books] ([isbn])
GO

ALTER TABLE [BorrowRecords]  WITH CHECK ADD FOREIGN KEY([user_id])
REFERENCES [Users] ([id])
GO

ALTER TABLE [BorrowRecords] ADD  DEFAULT (getdate()) FOR [borrow_date]
GO



USE [library]
GO
-- ����Ա��Ϣ
INSERT INTO [admins] (name, password) VALUES
(N'admin1', N'123456'),
(N'admin2', N'123456')

GO
INSERT INTO [Users] (name, tel) VALUES
(N'�Ŷ���', N'13700000001'),
(N'�����', N'13700000002'),
(N'������', N'13700000003'),
(N'�¶���', N'13700000004'),
(N'�ܶ���', N'13700000005'),
(N'�����', N'13700000006'),
(N'֣����', N'13700000007'),
(N'������', N'13700000008'),
(N'�Զ���', N'13700000009'),
(N'�����', N'13700000010');
GO
-- ������Ϣ
INSERT INTO [Authors] (name) VALUES
(N'����'),
(N'����'),
(N'����'),
(N'����'),
(N'����'),
(N'���'),
(N'֣��'),
(N'��ʮ');
GO

-- �����Ϣ
INSERT INTO [Categories] (name) VALUES
(N'��ѧ'),
(N'�ƻ�'),
(N'����'),
(N'����'),
(N'����'),
(N'����'),
(N'��ѧ');

GO
-- �鼮��Ϣ
INSERT INTO [Books] (ISBN, title, author_id, category_id, status) VALUES
('9787501522772', N'����', 4, 1, '�ɽ�'),
('9787532772857', N'����¶�', 5, 1, '�ɽ�'),
('9787532772858', N'Ų����ɭ��', 6, 1, '�ѽ��'),
('9787115454732', N'����', 7, 2, '�ɽ�'),
('9787536674512', N'���Ǿ�Ԯ', 8, 2, '�ɽ�'),
('9787115426548', N'�����Ĺ���', 8, 3, '�ɽ�'),
('9787544270868', N'��������ʷ', 6, 3, '�ɽ�'),
('9787300229279', N'����ѧԭ��', 5, 4, '�ѽ��'),
('9787300229280', N'����ѧ', 3, 4, '�ɽ�'),
('9787301278644', N'�л����񹲺͹��ܷ�', 8, 5, '�ɽ�'),
('9787301278645', N'�񷨵�', 7, 5, '�ɽ�'),
('9787300256254', N'�ִ�����ѧ', 2, 6, '�ѽ��'),
('9787300256255', N'��������ѧ', 8, 6, '�ɽ�'),
('9787300256256', N'������ѧʷ', 8, 7, '�ɽ�'),
('9787300256257', N'�й���ѧ��ʷ', 8, 7, '�ɽ�');
GO