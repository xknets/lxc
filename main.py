import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import pymssql


# main.py

from windows.book_manage import create_book_manage
from windows.login import create_login
from windows.windows_main import create_windows_main





def main():
    root = tk.Tk()
    # create_book_manage(root)
    create_login(root)
    # create_windows_main(root)
    root.mainloop()

if __name__ == "__main__":
    main()