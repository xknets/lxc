import tkinter as tk
from tkinter import messagebox
from util import connect_db
from windows.windows_main import create_windows_main

def create_login(parent):


    # 创建窗口
    global  root
    root = parent

    def login():
        try:
            username = entry_username.get()
            password = entry_password.get()

            # 检查用户名和密码是否为空
            if not username or not password:
                raise ValueError("用户名和密码不能为空，请输入完整信息！")

            # 连接数据库
            conn = connect_db()
            cursor = conn.cursor()

            # 获取分类ID
            cursor.execute("SELECT name,password FROM admins WHERE name = %s", (username,))
            info = cursor.fetchone()
            print(info) #调试用
            if not info:
                return messagebox.showinfo("警告", "用户名不存在，请重新输入！")


            # 这里可以加入实际的登录验证逻辑
            if username == info[0] and password == info[1]:
                # messagebox.showinfo("成功", "登录成功！")
                root.destroy()
                root2 = tk.Tk()
                create_windows_main(root2)
            else:
                messagebox.showerror("错误", "用户名或密码错误，请重试。")
        except ValueError as e:
            messagebox.showwarning("警告", str(e))

    def cancel():
        root.destroy()

    # 创建主窗口
    # root = tk.Tk()
    root.title("登录对话框")
    root.geometry("300x150")  # 设置窗口大小

    # 创建标签
    label_username = tk.Label(root, text="用户名:")
    label_username.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)

    label_password = tk.Label(root, text="密码:")
    label_password.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)

    # 创建输入框
    entry_username = tk.Entry(root)
    entry_username.grid(row=0, column=1, padx=10, pady=5)

    entry_password = tk.Entry(root, show="*")  # 密码输入框，隐藏输入内容
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    # 创建按钮
    button_login = tk.Button(root, text="登录", command=login)
    button_login.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)

    button_cancel = tk.Button(root, text="取消", command=cancel)
    button_cancel.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

    # 启动主循环
    # root.mainloop()