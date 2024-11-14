import tkinter as tk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, master):
        self.master = master
        self.logged_in = False

        self.top = tk.Toplevel(master)
        self.top.title("登录")

        self.username_label = tk.Label(self.top, text="用户名:")
        self.username_entry = tk.Entry(self.top)
        self.password_label = tk.Label(self.top, text="密码:")
        self.password_entry = tk.Entry(self.top, show="*")

        self.login_button = tk.Button(self.top, text="登录", command=self.login)

        self.username_label.grid(row=0, column=0)
        self.username_entry.grid(row=0, column=1)
        self.password_label.grid(row=1, column=0)
        self.password_entry.grid(row=1, column=1)
        self.login_button.grid(row=2, column=0, columnspan=2)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # 这里可以添加实际的验证逻辑
        if username == "admin" and password == "password":
            self.logged_in = True
            self.top.destroy()
        else:
            messagebox.showerror("错误", "用户名或密码错误")

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
