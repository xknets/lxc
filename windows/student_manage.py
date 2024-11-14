import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from util import connect_db,connect_close
import pymssql

#全局变量
root = 0
tree = 0

book_manage_opened = False
def get_book_m_opened():
    return book_manage_opened

def set_book_m_opened(sta):
    global book_manage_opened
    book_manage_opened = sta

# 查询所有数据
def fetch_data():
    conn = connect_db()
    cursor = conn.cursor()
    # cursor.execute("SELECT * FROM Books")
    cursor.execute("""
    select books.isbn,books.title,Authors.name,Categories.name, books.status 
    from books join Authors on books.author_id=authors.id 
    join Categories on Categories.id = books.category_id 
    """)
    data = cursor.fetchall()
    cursor.close()
    connect_close(conn)
    return data

# 更新 Treeview
def update_treeview(data):
    for row in tree.get_children():
        tree.delete(row)

    for item in data:
        tree.insert('', 'end', values=item)

# 删除记录
def delete_record():
    try:
        # 检查是否有选中的项目
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请选择一条记录")
            return

        # 获取选中项目的ISBN
        selected_isbn = str(tree.item(selected_item)['values'][0])
        print(f"被选中isbn：{selected_isbn}")

        # 连接数据库
        conn = connect_db()

        # 创建游标
        cursor = conn.cursor()


        # 执行删除操作
        cursor.execute("DELETE FROM Books WHERE isbn=%s", (selected_isbn,))

        # 提交事务
        conn.commit()

    # except pymssql.MySQLError as e:
    #     # 数据库操作出错，回滚事务
    #     conn.rollback()
    #     messagebox.showerror("数据库错误", f"发生错误: {e}")

    except Exception as e:
        # 其他未知错误
        messagebox.showerror("未知错误", f"发生未知错误: {e}")

    except pymssql.exceptions.OperationalError as e:
        # 其他未知错误
        messagebox.showerror("未知错误", f"发生未知错误: {e}")

    finally:
        # 关闭游标和连接
        if cursor:
            cursor.close()
        connect_close(conn)

        # 更新TreeView控件显示的数据
        update_treeview(fetch_data())
#


def fetch_a_c_data():
    conn = connect_db()
    cursor = conn.cursor()

    # 获取作者名字
    cursor.execute("SELECT id, name FROM Authors")
    authors = cursor.fetchall()

    # 获取分类名称
    cursor.execute("SELECT id, name FROM Categories")
    categories = cursor.fetchall()

    cursor.close()
    connect_close(conn)

    return authors, categories


def add_record():
    def submit():
        isbn = entry_isbn.get().strip()
        title = entry_title.get().strip()
        author_name = combo_author.get().strip()
        category_name = combo_category.get().strip()
        status = combo_status.get().strip()
        print(isbn,title,author_name,category_name,status)
        try:
            # 验证输入
            if not (isbn and title and author_name and category_name and status):
                raise ValueError("请确保所有字段都已正确填写")

            # 连接数据库
            conn = connect_db()
            cursor = conn.cursor()

            # 获取分类ID
            cursor.execute("SELECT isbn FROM Books WHERE isbn = %s", (isbn,))
            isbn1 = cursor.fetchone()
            if isbn1:
                raise ValueError("isbn重复！请确认后输入")


            # 获取作者ID
            cursor.execute("SELECT id FROM Authors WHERE name = %s", (author_name,))
            author_id = cursor.fetchone()

            if not author_id:
                # 新增作者记录
                cursor.execute("INSERT INTO Authors (name) VALUES (%s)", (author_name,))
                conn.commit()
                # 获取新插入的作者ID
                cursor.execute("SELECT id FROM Authors WHERE name = %s", (author_name,))
                author_id = cursor.fetchone()[0]
            else:
                author_id = author_id[0]

            # 获取分类ID
            cursor.execute("SELECT id FROM Categories WHERE name = %s", (category_name,))
            category_id = cursor.fetchone()
            if not category_id:
                # 新增分类记录
                cursor.execute("INSERT INTO Categories (name) VALUES (%s)", (category_name,))
                conn.commit()
                # 获取新插入的分类ID
                cursor.execute("SELECT id FROM Categories WHERE name = %s", (category_name,))
                category_id = cursor.fetchone()[0]
            else:
                category_id = category_id[0]

            # 执行插入操作
            cursor.execute("INSERT INTO Books (isbn,title, author_id, category_id, status) VALUES (%s, %s, %s, %s, %s)",
                           (isbn, title, author_id, category_id, status))

            # 提交事务
            conn.commit()

            # 关闭游标和连接
            cursor.close()
            connect_close(conn)

            # 更新TreeView控件显示的数据
            update_treeview(fetch_data())

            # 关闭输入窗口
            input_window.destroy()

        except ValueError as e:
            messagebox.showerror("输入错误", f"输入格式错误: {e}")
        except pymssql.MySQLError as e:
            # 数据库操作出错，回滚事务
            conn.rollback()
            messagebox.showerror("数据库错误", f"发生错误: {e}")
        except Exception as e:
            # 其他未知错误
            messagebox.showerror("未知错误", f"发生未知错误: {e}")

    # 创建输入窗口
    input_window = tk.Toplevel(root)
    input_window.title("添加记录")

    # 获取作者和分类数据
    authors, categories = fetch_a_c_data()

    # 创建输入框和标签
    label_isbn = tk.Label(input_window, text="书号:")
    label_isbn.grid(row=0, column=0, padx=5, pady=5)
    entry_isbn = tk.Entry(input_window)
    entry_isbn.grid(row=0, column=1, padx=5, pady=5)

    label_title = tk.Label(input_window, text="书名:")
    label_title.grid(row=1, column=0, padx=5, pady=5)
    entry_title = tk.Entry(input_window)
    entry_title.grid(row=1, column=1, padx=5, pady=5)

    label_author = tk.Label(input_window, text="作者:")
    label_author.grid(row=2, column=0, padx=5, pady=5)
    combo_author = ttk.Combobox(input_window, values=[author[1] for author in authors])
    combo_author.grid(row=2, column=1, padx=5, pady=5)

    label_category = tk.Label(input_window, text="分类:")
    label_category.grid(row=3, column=0, padx=5, pady=5)
    combo_category = ttk.Combobox(input_window, values=[category[1] for category in categories])
    combo_category.grid(row=3, column=1, padx=5, pady=5)

    # label_status = tk.Label(input_window, text="状态:")
    # label_status.grid(row=3, column=0, padx=5, pady=5)
    # entry_status = tk.Entry(input_window)
    # entry_status.grid(row=3, column=1, padx=5, pady=5)
    label_status = tk.Label(input_window, text="状态:")
    label_status.grid(row=4, column=0, padx=5, pady=5)
    combo_status = ttk.Combobox(input_window, values=['可借', '已借出'])
    combo_status.set('可借')  # 设置默认值
    combo_status.grid(row=4, column=1, padx=5, pady=5)


    # 创建提交按钮
    button_submit = tk.Button(input_window, text="提交", command=submit)
    button_submit.grid(row=5, column=0, columnspan=2, pady=10)

# 修改记录
# 修改记录
def edit_record():
    def submit():
        title = entry_title.get().strip()
        author_name = combo_author.get().strip()
        category_name = combo_category.get().strip()
        status = combo_status.get().strip()

        try:
            # 验证输入
            if not (title and author_name and category_name and status):
                raise ValueError("请确保所有字段都已正确填写")

            # 连接数据库
            conn = connect_db()
            cursor = conn.cursor()

            # 获取作者ID
            cursor.execute("SELECT id FROM Authors WHERE name = %s", (author_name,))
            author_id = cursor.fetchone()

            if not author_id:
                # 新增作者记录
                cursor.execute("INSERT INTO Authors (name) VALUES (%s)", (author_name,))
                conn.commit()
                # 获取新插入的作者ID
                cursor.execute("SELECT id FROM Authors WHERE name = %s", (author_name,))
                author_id = cursor.fetchone()[0]
            else:
                author_id = author_id[0]

            # 获取分类ID
            cursor.execute("SELECT id FROM Categories WHERE name = %s", (category_name,))
            category_id = cursor.fetchone()
            if not category_id:
                # 新增分类记录
                cursor.execute("INSERT INTO Categories (name) VALUES (%s)", (category_name,))
                conn.commit()
                # 获取新插入的分类ID
                cursor.execute("SELECT id FROM Categories WHERE name = %s", (category_name,))
                category_id = cursor.fetchone()[0]
            else:
                category_id = category_id[0]

            # 执行更新操作
            cursor.execute("UPDATE Books SET title=%s, author_id=%s, category_id=%s, status=%s WHERE isbn=%s",
                           (title, author_id, category_id, status, selected_id))

            # 提交事务
            conn.commit()

            # 关闭游标和连接
            cursor.close()
            connect_close(conn)

            # 更新TreeView控件显示的数据
            update_treeview(fetch_data())

            # 关闭输入窗口
            input_window.destroy()

        except ValueError as e:
            messagebox.showerror("输入错误", f"输入格式错误: {e}")
        except pymssql.MySQLError as e:
            # 数据库操作出错，回滚事务
            conn.rollback()
            messagebox.showerror("数据库错误", f"发生错误: {e}")
        except Exception as e:
            # 其他未知错误
            messagebox.showerror("未知错误", f"发生未知错误: {e}")

    # 检查是否选择了记录
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("警告", "请选择一条记录")
        return

    # 获取选中的记录ID
    selected_id = tree.item(selected_item)['values'][0]

    # 创建输入窗口
    input_window = tk.Toplevel(root)
    input_window.title("编辑记录")

    # 获取作者和分类数据
    authors, categories = fetch_a_c_data()

    # 获取当前记录的信息
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT title, author_id, category_id, status FROM Books WHERE isbn = %s", (selected_id,))
    book_info = cursor.fetchone()
    cursor.close()
    connect_close(conn)

    # 创建输入框和标签
    label_title = tk.Label(input_window, text="书名:")
    label_title.grid(row=0, column=0, padx=5, pady=5)
    entry_title = tk.Entry(input_window)
    entry_title.insert(0, book_info[0])
    entry_title.grid(row=0, column=1, padx=5, pady=5)

    label_author = tk.Label(input_window, text="作者:")
    label_author.grid(row=1, column=0, padx=5, pady=5)
    combo_author = ttk.Combobox(input_window, values=[author[1] for author in authors])
    combo_author.set([author[1] for author in authors if author[0] == book_info[1]][0])
    combo_author.grid(row=1, column=1, padx=5, pady=5)

    label_category = tk.Label(input_window, text="分类:")
    label_category.grid(row=2, column=0, padx=5, pady=5)
    combo_category = ttk.Combobox(input_window, values=[category[1] for category in categories])
    combo_category.set([category[1] for category in categories if category[0] == book_info[2]][0])
    combo_category.grid(row=2, column=1, padx=5, pady=5)

    label_status = tk.Label(input_window, text="状态:")
    label_status.grid(row=3, column=0, padx=5, pady=5)
    combo_status = ttk.Combobox(input_window, values=['可借', '已借出'])
    combo_status.set(book_info[3])  # 设置默认值
    combo_status.grid(row=3, column=1, padx=5, pady=5)

    # 创建提交按钮
    button_submit = tk.Button(input_window, text="提交", command=submit)
    button_submit.grid(row=4, column=0, columnspan=2, pady=10)


def query_record():
    def submit():
        query_type = combo_query_type.get().strip()
        query_value = entry_query_value.get().strip()

        if not (query_type and query_value):
            messagebox.showwarning("警告", "请输入查询条件")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            if query_type == "作者":
                cursor.execute("SELECT b.isbn, b.title, a.name AS author, c.name AS category, b.status FROM Books b JOIN Authors a ON b.author_id = a.id JOIN Categories c ON b.category_id = c.id WHERE a.name LIKE %s", (f"%{query_value}%",))
            elif query_type == "分类":
                cursor.execute("SELECT b.isbn, b.title, a.name AS author, c.name AS category, b.status FROM Books b JOIN Authors a ON b.author_id = a.id JOIN Categories c ON b.category_id = c.id WHERE c.name LIKE %s", (f"%{query_value}%",))
            elif query_type == "书名":
                cursor.execute("SELECT b.isbn, b.title, a.name AS author, c.name AS category, b.status FROM Books b JOIN Authors a ON b.author_id = a.id JOIN Categories c ON b.category_id = c.id WHERE b.title LIKE %s", (f"%{query_value}%",))
            data = cursor.fetchall()
            update_treeview(data)
        except Exception as e:
            messagebox.showerror("错误", f"查询条件无效：{e}")
        finally:
            cursor.close()
            connect_close(conn)
            query_window.destroy()

    def cancel():
        query_window.destroy()

    # 创建查询窗口
    query_window = tk.Toplevel(root)
    query_window.title("查询记录")

    # 创建下拉列表和标签
    label_query_type = tk.Label(query_window, text="查询类型:")
    label_query_type.grid(row=0, column=0, padx=5, pady=5)
    combo_query_type = ttk.Combobox(query_window, values=["作者", "分类", "书名"])
    combo_query_type.grid(row=0, column=1, padx=5, pady=5)

    # 创建输入框和标签
    label_query_value = tk.Label(query_window, text="查询内容:")
    label_query_value.grid(row=1, column=0, padx=5, pady=5)
    entry_query_value = tk.Entry(query_window)
    entry_query_value.grid(row=1, column=1, padx=5, pady=5)

    # 创建提交和取消按钮
    button_submit = tk.Button(query_window, text="确定", command=submit)
    button_submit.grid(row=2, column=0, padx=5, pady=5)
    button_cancel = tk.Button(query_window, text="取消", command=cancel)
    button_cancel.grid(row=2, column=1, padx=5, pady=5)

# 关闭窗体
def close_window():
    global book_manage_opened
    root.destroy()
    book_manage_opened = False
    print(book_manage_opened)

def create_book_manage(parent):
    # 创建窗口
    global  root
    root = parent

    # 绑定关闭事件
    root.protocol("WM_DELETE_WINDOW", lambda: close_window())

    root.title("图书管理系统")
    root.geometry('1000x400')

    # 创建 Treeview
    global  tree
    tree = ttk.Treeview(root, columns=("isbn", "title", "author_name", "category_name", "status"), show="headings")
    tree.heading("isbn", text="ISBN")
    tree.heading("title", text="书名")
    tree.heading("author_name", text="作者")
    tree.heading("category_name", text="类别")
    tree.heading("status", text="状态")
    # 添加垂直滚动条
    # vsb = ttk.Scrollbar(tree, orient="vertical", command=tree.yview)
    # vsb.pack(side=tk.RIGHT, fill=tk.Y)
    # tree.configure(yscrollcommand=vsb.set)

    
    

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # 初始化 Treeview
    update_treeview(fetch_data())

    # 创建按钮
    frame_buttons = ttk.Frame(root)
    frame_buttons.pack(pady=10)

    btn_delete = ttk.Button(frame_buttons, text="删除", command=delete_record)
    btn_add = ttk.Button(frame_buttons, text="新增", command=add_record)
    btn_edit = ttk.Button(frame_buttons, text="修改", command=edit_record)
    btn_query = ttk.Button(frame_buttons, text="查询", command=query_record)
    btn_close = ttk.Button(frame_buttons, text="关闭", command=close_window)

    btn_delete.grid(row=0, column=0, padx=5)
    btn_add.grid(row=0, column=1, padx=5)
    btn_edit.grid(row=0, column=2, padx=5)
    btn_query.grid(row=0, column=3, padx=5)
    btn_close.grid(row=0, column=4, padx=5)

