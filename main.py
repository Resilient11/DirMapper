import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, folder_path)

def start_listing():
    folder_path = entry_path.get().strip()
    if not folder_path or not os.path.isdir(folder_path):
        messagebox.showwarning("路径无效", "请选择一个有效的文件夹！")
        return 

    try:
        depth = int(entry_depth.get())
        if depth < 1:
            raise ValueError("深度必须 ≥ 1")
    except ValueError:
        messagebox.showerror("输入错误", "请输入有效的正整数作为遍历深度！")
        return

    list_files_and_folders(folder_path, depth)

def list_files_and_folders(folder_path, max_depth):
    text_output.delete(1.0, tk.END)
    try:
        for root, dirs, files in os.walk(folder_path):
            # Calculate level: selected folder is level 1
            if root == folder_path:
                level = 1
            else:
                level = root[len(folder_path):].count(os.sep) + 1
                # Ensure no negative
                if level < 1:
                    level = 1

            if level > max_depth:
                dirs.clear()
                continue

            # Display folder
            if level == 1:
                folder_name = os.path.basename(folder_path) or folder_path
                indent = "├── "
            else:
                indent = "│   " * (level - 1) + "├── "
                folder_name = os.path.basename(root)
            text_output.insert(tk.END, f"{indent}[{folder_name}]\n")

            # Display files only if not at the max depth
            if level < max_depth:
                for file in files:
                    file_indent = "│   " * level + "├── "
                    text_output.insert(tk.END, f"{file_indent}{file}\n")

            # Prevent deeper recursion at max depth
            if level == max_depth:
                dirs.clear()

    except OSError as e:
        text_output.insert(tk.END, f"无法读取文件夹 {folder_path}: {e}\n")

# GUI setup
root = tk.Tk()
root.title("文件夹内容查看工具（支持深度控制）")
root.geometry("750x550")

root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(1, weight=1)

tk.Label(root, text="文件夹路径:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
entry_path = tk.Entry(root)
entry_path.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
btn_select = tk.Button(root, text="选择...", command=select_folder)
btn_select.grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="遍历深度:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
entry_depth = tk.Entry(root, width=10)
entry_depth.insert(0, "1")
entry_depth.grid(row=1, column=1, padx=10, pady=5, sticky="w")

btn_start = tk.Button(root, text="开始遍历", command=start_listing, bg="#4CAF50", fg="white")
btn_start.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Consolas", 10))
text_output.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky="nsew")

root.mainloop()
