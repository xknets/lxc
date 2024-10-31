import tkinter as tk
from windows.book_manage import create_book_manage,get_book_m_opened,set_book_m_opened


book_manage_opened = False

def create_windows_main(parent):
    # 创建窗口
    global  root
    root = parent

    def reader_management():
        print("读者管理")

    def book_management():
        print("图书管理")
       ## root.destroy()
        b_open = get_book_m_opened()
        if not b_open:
            root2 = tk.Tk()
            create_book_manage(root2)
            set_book_m_opened(True)
        else:
            return

    def borrow_book():
        print("借书")

    def return_book():
        print("还书")

    root.title("图书管理系统")

    # 设置窗口大小
    root.geometry("350x400")

    # 创建标签
    label = tk.Label(root, text="图书管理系统", font=("黑体", 23,"bold"))
    # label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.NW)
    label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky=tk.N + tk.E + tk.S + tk.W)

    # 加载图片
    try:
        image_path = "main.gif"  # 替换为你的图片路径，必须是GIF格式
        photo = tk.PhotoImage(file=image_path)
    except Exception as e:
        print(f"加载图片时出错: {e}")
        photo = None

    # 创建图片标签
    if photo:
        image_label = tk.Label(root, image=photo)
        image_label.image = photo  # 保持引用，防止垃圾回收
        image_label.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky=tk.NW)
    else:
        image_label = tk.Label(root, text="无法加载图片")
        image_label.grid(row=1, column=0, rowspan=4, padx=10, pady=10, sticky=tk.NW)

    global root2
    root2 =None
    # 创建按钮
    btn_reader = tk.Button(root, text="读者管理", command=reader_management, font=("黑体", 16,"bold"))
    btn_reader.grid(row=1, column=1, padx=10, pady=10, sticky=tk.E)

    btn_book = tk.Button(root, text="图书管理", command=book_management, font=("黑体", 16,"bold"))
    btn_book.grid(row=2, column=1, padx=10, pady=10, sticky=tk.E)

    btn_borrow = tk.Button(root, text="借书", command=borrow_book, font=("黑体", 16,"bold"))
    btn_borrow.grid(row=3, column=1, padx=10, pady=10, sticky=tk.E)

    btn_return = tk.Button(root, text="还书", command=return_book, font=("黑体", 16,"bold"))
    btn_return.grid(row=4, column=1, padx=10, pady=10, sticky=tk.E)