import tkinter as tk
from tkinter import messagebox
from ..util import add_student, query_students, delete_student

def main_window():
    root = tk.Tk()
    root.title("学生信息管理系统")

    # 菜单栏
    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="文件", menu=file_menu)
    file_menu.add_command(label="退出", command=root.quit)

    # 功能按钮
    btn_add_student = tk.Button(root, text="添加学生", command=add_student_window)
    btn_query_students = tk.Button(root, text="查询学生", command=query_students_window)
    btn_delete_student = tk.Button(root, text="删除学生", command=delete_student_window)

    btn_add_student.pack(pady=5)
    btn_query_students.pack(pady=5)
    btn_delete_student.pack(pady=5)

    root.mainloop()

def add_student_window():
    add_window = tk.Toplevel()
    add_window.title("添加学生")

    # 输入框
    name_label = tk.Label(add_window, text="姓名:")
    name_entry = tk.Entry(add_window)
    gender_label = tk.Label(add_window, text="性别:")
    gender_entry = tk.Entry(add_window)
    admission_year_label = tk.Label(add_window, text="入学年度:")
    admission_year_entry = tk.Entry(add_window)
    hometown_label = tk.Label(add_window, text="籍贯:")
    hometown_entry = tk.Entry(add_window)
    major_label = tk.Label(add_window, text="专业名:")
    major_entry = tk.Entry(add_window)
    class_name_label = tk.Label(add_window, text="班级名:")
    class_name_entry = tk.Entry(add_window)

    # 布局
    name_label.grid(row=0, column=0)
    name_entry.grid(row=0, column=1)
    gender_label.grid(row=1, column=0)
    gender_entry.grid(row=1, column=1)
    admission_year_label.grid(row=2, column=0)
    admission_year_entry.grid(row=2, column=1)
    hometown_label.grid(row=3, column=0)
    hometown_entry.grid(row=3, column=1)
    major_label.grid(row=4, column=0)
    major_entry.grid(row=4, column=1)
    class_name_label.grid(row=5, column=0)
    class_name_entry.grid(row=5, column=1)

    # 提交按钮
    submit_button = tk.Button(add_window, text="提交", command=lambda: add_student(
        name_entry.get(),
        gender_entry.get(),
        int(admission_year_entry.get()),
        hometown_entry.get(),
        major_entry.get(),
        class_name_entry.get()
    ))
    submit_button.grid(row=6, column=0, columnspan=2)

def query_students_window():
    query_window = tk.Toplevel()
    query_window.title("查询学生")

    # 结果显示
    result_text = tk.Text(query_window, height=10, width=50)
    result_text.grid(row=0, column=0, columnspan=2)

    # 查询按钮
    query_button = tk.Button(query_window, text="查询", command=lambda: perform_query(result_text))
    query_button.grid(row=1, column=0, columnspan=2)

    def perform_query(result_text):
        results = query_students()
        result_text.delete(1.0, tk.END)
        for row in results:
            result_text.insert(tk.END, str(row) + "\n")

def delete_student_window():
    delete_window = tk.Toplevel()
    delete_window.title("删除学生")

    # 输入框
    student_id_label = tk.Label(delete_window, text="学生ID:")
    student_id_entry = tk.Entry(delete_window)

    # 布局
    student_id_label.grid(row=0, column=0)
    student_id_entry.grid(row=0, column=1)

    # 提交按钮
    submit_button = tk.Button(delete_window, text="提交", command=lambda: delete_student(
        int(student_id_entry.get())
    ))
    submit_button.grid(row=1, column=0, columnspan=2)

if __name__ == "__main__":
    main_window()
