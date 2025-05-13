# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
from filesystem import FileSystem

class FileSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("File System Simulator")
        self.fs = FileSystem()

        tk.Label(root, text="File Name:").grid(row=0, column=0)
        self.file_entry = tk.Entry(root)
        self.file_entry.grid(row=0, column=1)

        tk.Label(root, text="Size:").grid(row=1, column=0)
        self.size_entry = tk.Entry(root)
        self.size_entry.grid(row=1, column=1)

        tk.Label(root, text="Allocation Method:").grid(row=2, column=0)
        self.method_var = tk.StringVar(value="contiguous")
        self.method_dropdown = ttk.Combobox(root, textvariable=self.method_var, values=["contiguous", "linked", "indexed"])
        self.method_dropdown.grid(row=2, column=1)

        tk.Label(root, text="Scheduling Algorithm:").grid(row=3, column=0)
        self.scheduling_var = tk.StringVar(value="FCFS")
        self.scheduling_dropdown = ttk.Combobox(root, textvariable=self.scheduling_var, values=["FCFS", "SSTF", "SCAN"])
        self.scheduling_dropdown.grid(row=3, column=1)
        tk.Button(root, text="Set Scheduling", command=self.set_scheduling).grid(row=3, column=2)

        tk.Label(root, text="File Content:").grid(row=4, column=0)
        self.content_text = tk.Text(root, height=5, width=40)
        self.content_text.grid(row=4, column=1, columnspan=2)

        tk.Button(root, text="Create File", command=self.create_file).grid(row=5, column=0)
        tk.Button(root, text="Delete File", command=self.delete_selected_file).grid(row=5, column=1)
        tk.Button(root, text="List Files", command=self.list_files).grid(row=6, column=0)
        tk.Button(root, text="Write Content", command=self.write_content).grid(row=6, column=1)
        tk.Button(root, text="Read Content", command=self.read_content).grid(row=6, column=2)

        self.file_listbox = tk.Listbox(root, height=5, width=40)
        self.file_listbox.grid(row=7, column=0, columnspan=2)

        self.output = tk.Text(root, height=10, width=50)
        self.output.grid(row=8, column=0, columnspan=3)

        # Disk visualization
        self.canvas = tk.Canvas(root, width=400, height=100)
        self.canvas.grid(row=10, column=0, columnspan=3)
        self.update_disk_visualization()

    def log_output(self, message):
        self.output.config(state=tk.NORMAL)
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.output.config(state=tk.DISABLED)

    def set_scheduling(self):
        method = self.scheduling_var.get()
        self.fs.set_scheduling_method(method)
        self.log_output(f"Scheduling method set to {method}")

    def create_file(self):
        filename = self.file_entry.get().strip()
        size = self.size_entry.get().strip()
        method = self.method_var.get()

        if not filename or not size:
            messagebox.showerror("Error", "Filename and size are required.")
            return
        if not size.isdigit():
            messagebox.showerror("Error", "Size must be a number.")
            return

        result = self.fs.create_file(filename, int(size), method)
        self.log_output(result)
        self.list_files()
        self.update_disk_visualization()

    def delete_selected_file(self):
        selected = self.file_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "No file selected.")
            return
        filename = self.file_listbox.get(selected[0])
        result = self.fs.delete_file(filename)
        self.log_output(result)
        self.list_files()
        self.update_disk_visualization()

    def write_content(self):
        filename = self.file_entry.get().strip()
        content = self.content_text.get("1.0", tk.END).strip()
        result = self.fs.write_to_file(filename, content)
        self.log_output(result)

    def read_content(self):
        filename = self.file_entry.get().strip()
        result = self.fs.read_file(filename)
        self.log_output(f"{filename} content: {result}")

    def list_files(self):
        self.file_listbox.delete(0, tk.END)
        files = self.fs.list_files()
        for file in files:
            self.file_listbox.insert(tk.END, file)
        self.log_output("\n".join(files))

    def update_disk_visualization(self):
        self.canvas.delete("all")
        disk_visual = self.fs.get_free_space_visual()
        block_width = 4
        for i, block in enumerate(disk_visual):
            color = "green" if block == "#" else "red"
            self.canvas.create_rectangle(i * block_width, 10, (i + 1) * block_width, 60, fill=color, outline="black")
