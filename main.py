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

    folder_path = os.path.abspath(os.path.normpath(folder_path))
    root_name = os.path.basename(folder_path) or folder_path

    text_output.insert(tk.END, f"[{root_name}]\n")

    def walk_dir(path, depth):
        if depth > max_depth:
            return

        try:
            entries = list(os.scandir(path))
        except OSError as e:
            indent = "│   " * depth
            text_output.insert(tk.END, f"{indent}无法读取: {e}\n")
            return

        dirs = sorted([e for e in entries if e.is_dir(follow_symlinks=False)], key=lambda x: x.name.lower())
        files = sorted([e for e in entries if e.is_file(follow_symlinks=False)], key=lambda x: x.name.lower())

        all_items = dirs + files

        for index, item in enumerate(all_items):
            is_last = index == len(all_items) - 1
            prefix = "└── " if is_last else "├── "
            indent = "│   " * (depth - 1)

            if item.is_dir(follow_symlinks=False):
                text_output.insert(tk.END, f"{indent}{prefix}[{item.name}]\n")

                if depth < max_depth:
                    walk_dir(item.path, depth + 1)
            else:
                text_output.insert(tk.END, f"{indent}{prefix}{item.name}\n")

    walk_dir(folder_path, 1)

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

