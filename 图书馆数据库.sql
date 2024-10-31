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
	[status] [nvarchar](50) CHECK([status]= '可借' OR [status] = '已借出') NOT NULL,

) 

GO

ALTER TABLE [Books]  WITH CHECK ADD FOREIGN KEY([author_id])
REFERENCES [Authors] ([id])
GO

ALTER TABLE [Books]  WITH CHECK ADD FOREIGN KEY([category_id])
REFERENCES [Categories] ([id])
GO

ALTER TABLE [Books] ADD  DEFAULT ('可借') FOR [status]
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
-- 管理员信息
INSERT INTO [admins] (name, password) VALUES
(N'admin1', N'123456'),
(N'admin2', N'123456')

GO
INSERT INTO [Users] (name, tel) VALUES
(N'张读者', N'13700000001'),
(N'李读者', N'13700000002'),
(N'王读者', N'13700000003'),
(N'陈读者', N'13700000004'),
(N'周读者', N'13700000005'),
(N'吴读者', N'13700000006'),
(N'郑读者', N'13700000007'),
(N'刘读者', N'13700000008'),
(N'赵读者', N'13700000009'),
(N'孙读者', N'13700000010');
GO
-- 作者信息
INSERT INTO [Authors] (name) VALUES
(N'张三'),
(N'李四'),
(N'王五'),
(N'陈六'),
(N'周七'),
(N'吴八'),
(N'郑九'),
(N'刘十');
GO

-- 类别信息
INSERT INTO [Categories] (name) VALUES
(N'文学'),
(N'科幻'),
(N'艺术'),
(N'经济'),
(N'法律'),
(N'教育'),
(N'哲学');

GO
-- 书籍信息
INSERT INTO [Books] (ISBN, title, author_id, category_id, status) VALUES
('9787501522772', N'活着', 4, 1, '可借'),
('9787532772857', N'百年孤独', 5, 1, '可借'),
('9787532772858', N'挪威的森林', 6, 1, '已借出'),
('9787115454732', N'三体', 7, 2, '可借'),
('9787536674512', N'火星救援', 8, 2, '可借'),
('9787115426548', N'艺术的故事', 8, 3, '可借'),
('9787544270868', N'西方美术史', 6, 3, '可借'),
('9787300229279', N'经济学原理', 5, 4, '已借出'),
('9787300229280', N'金融学', 3, 4, '可借'),
('9787301278644', N'中华人民共和国宪法', 8, 5, '可借'),
('9787301278645', N'民法典', 7, 5, '可借'),
('9787300256254', N'现代教育学', 2, 6, '已借出'),
('9787300256255', N'教育心理学', 8, 6, '可借'),
('9787300256256', N'西方哲学史', 8, 7, '可借'),
('9787300256257', N'中国哲学简史', 8, 7, '可借');
GO