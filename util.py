import pymssql


server = 'localhost'  # 使用配置文件中的服务器名称
username = 'sa'  # 使用你的 Windows 用户名
password = '123456'  # 如果不需要密码则留空


# 连接数据库
def connect_db():
    # 连接数据库，如果失败抛出pymssql.OperationalError异常

    database_name='library'
    # 创建连接
    try:
        conn = pymssql.connect(server=server, user=username, password=password, database=database_name)
    except pymssql.OperationalError as e:  # 有异常执行
        print(f"Connection failed: {e}")
        raise  # 抛出捕获到的异常
    else:  # 没有异常执行
        print(f"数据库{database_name}已连接！")
        return conn

#关闭数据库，如果失败则打印提示
def connect_close(conn):
    # 关闭连接
    try:
        if conn:
            conn.close()
            print("连接已关闭")
    except Exception as e:
        print(f"关闭连接时发生错误: {e}")
