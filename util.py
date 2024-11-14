import pyodbc

def connect_to_db():
    # 定义连接字符串，包括服务器名、数据库名、用户名和密码
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=your_server_name;'  # 替换为你的服务器名
        'DATABASE=StudentManagementSystem;'
        'UID=your_username;'        # 替换为你的用户名
        'PWD=your_password'         # 替换为你的密码
    )
    # 建立连接
    conn = pyodbc.connect(conn_str)
    return conn

def add_student(name, gender, admission_year, hometown, major, class_name):
    conn = connect_to_db()  # 连接到数据库
    cursor = conn.cursor()  # 创建游标
    # 执行插入语句
    cursor.execute("""
        INSERT INTO Students (name, gender, admission_year, hometown, major, class_name)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, gender, admission_year, hometown, major, class_name))
    conn.commit()  # 提交事务
    conn.close()   # 关闭连接

def query_students():
    conn = connect_to_db()  # 连接到数据库
    cursor = conn.cursor()  # 创建游标
    # 执行查询语句
    cursor.execute("SELECT * FROM Students")
    rows = cursor.fetchall()  # 获取所有行
    conn.close()  # 关闭连接
    return rows  # 返回查询结果

def delete_student(student_id):
    conn = connect_to_db()  # 连接到数据库
    cursor = conn.cursor()  # 创建游标
    # 执行删除语句
    cursor.execute("DELETE FROM Students WHERE student_id = ?", (student_id,))
    conn.commit()  # 提交事务
    conn.close()   # 关闭连接
