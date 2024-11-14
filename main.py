import tkinter as tk
from windows.login import LoginWindow
from windows.student_manage import main_window

def start_application():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    login_window = LoginWindow(root)
    root.wait_window(login_window.top)  # 等待登录窗口关闭

    if login_window.logged_in:
        main_window()

if __name__ == "__main__":
    start_application()
