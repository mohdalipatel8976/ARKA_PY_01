import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ToDoListApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("450x500")
        self.title("To-Do List")
        self.style = ttk.Style(self)
        self.configure_styles()

        self.create_widget()

    def configure_styles(self):
        self.style.configure("TButton",
                             padding=6,
                             relief="flat",
                             background="#ccc",
                             font=("Arial", 10))

        self.style.map("TButton",
                       foreground=[('pressed', 'black'), ('active', 'blue')],
                       background=[('pressed', '!disabled', 'grey'), ('active', 'white')])

        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TLabelFrame", background="#f0f0f0")
        self.style.configure("TLabel", background="#f0f0f0")

    def create_widget(self):
        task_frame = ttk.LabelFrame(self, text="New Task", padding=(10, 10))
        task_frame.pack(pady=10, padx=10, fill="x")

        self.task_input = ttk.Entry(task_frame, width=30)
        self.task_input.pack(side="left", padx=(0, 10))

        self.add_task_button = ttk.Button(task_frame, text="Add Task", command=self.add_task)
        self.add_task_button.pack(side="left")

        self.tasks_listbox = tk.Listbox(self,
                                         selectmode=tk.SINGLE,
                                         height=10,
                                         font=("Arial", 12),
                                         activestyle='none',
                                         highlightthickness=0,
                                         relief='flat')
        self.tasks_listbox.pack(pady=10, padx=10, fill="both", expand=True)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)

        self.edit_task_button = ttk.Button(button_frame, text="Edit Task", command=self.open_edit_dialog)
        self.edit_task_button.grid(row=0, column=0, padx=5, pady=5)

        self.delete_task_button = ttk.Button(button_frame, text="Delete Task", command=self.delete_task)
        self.delete_task_button.grid(row=0, column=1, padx=5, pady=5)

        self.mark_done_button = ttk.Button(button_frame, text="Mark Done", command=self.mark_done)
        self.mark_done_button.grid(row=0, column=2, padx=5, pady=5)

        self.mark_not_done_button = ttk.Button(button_frame, text="Mark Not Done", command=self.mark_not_done)
        self.mark_not_done_button.grid(row=0, column=3, padx=5, pady=5)

        self.save_button = ttk.Button(button_frame, text="Save Tasks", command=self.save_task)
        self.save_button.grid(row=1, column=1, padx=5, pady=5)

        self.load_button = ttk.Button(button_frame, text="Load Tasks", command=self.load_tasks)
        self.load_button.grid(row=1, column=2, padx=5, pady=5)

    def add_task(self):
        task = self.task_input.get().strip()
        if task:
            self.tasks_listbox.insert(tk.END, task)
            task_index = self.tasks_listbox.size() - 1
            self.tasks_listbox.itemconfig(task_index, {'bg': 'yellow'})
            self.task_input.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task.")

    def open_edit_dialog(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
            task_text = self.tasks_listbox.get(task_index)
            task_bg = self.tasks_listbox.itemcget(task_index, 'bg')

            edit_window = tk.Toplevel(self)
            edit_window.title("Edit Task")
            edit_window.grab_set()

            x = self.winfo_x()
            y = self.winfo_y()
            edit_window.geometry(f"+{x + 100}+{y + 100}")

            edit_label = ttk.Label(edit_window, text="Edit Task:")
            edit_label.pack(pady=10)

            edit_entry = ttk.Entry(edit_window, width=40)
            edit_entry.insert(0, task_text)  
            edit_entry.pack(pady=10)

            def save_changes():
                new_task = edit_entry.get().strip()
                if new_task:
                    self.tasks_listbox.delete(task_index)
                    self.tasks_listbox.insert(task_index, new_task)
                    self.tasks_listbox.itemconfig(task_index, {'bg': task_bg})  
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Input Error", "Please enter the updated task.")

            save_button = ttk.Button(edit_window, text="Save", command=save_changes)
            save_button.pack(pady=10)

        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to edit.")

    def delete_task(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")
            return

        confirm = messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete the selected task?")
        if confirm:
            self.tasks_listbox.delete(task_index)

    def mark_done(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.itemconfig(task_index, {'bg': 'light green'})
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as done.")

    def mark_not_done(self):
        try:
            task_index = self.tasks_listbox.curselection()[0]
            self.tasks_listbox.itemconfig(task_index, {'bg': 'yellow'})
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to mark as not done.")

    def save_task(self):
        tasks = self.tasks_listbox.get(0, tk.END)
        if not tasks:
            messagebox.showwarning("Save Error", "No tasks to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension='.txt',
                                                 filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for index, task in enumerate(tasks):
                    status = self.tasks_listbox.itemcget(index, 'bg')
                    file.write(f"{task}|{status}\n")
            messagebox.showinfo("Save Success", "Tasks saved successfully!")

    def load_tasks(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                tasks = file.readlines()

            self.tasks_listbox.delete(0, tk.END)
            for line in tasks:
                if '|' in line:
                    task, status = line.strip().split('|', 1)
                else:
                    task = line.strip()
                    status = 'yellow' 
                self.tasks_listbox.insert(tk.END, task)
                task_index = self.tasks_listbox.size() - 1
                self.tasks_listbox.itemconfig(task_index, {'bg': status})
            messagebox.showinfo("Load Success", "Tasks loaded successfully!")
        else:
            messagebox.showwarning("Load Error", "No file selected.")


if __name__ == "__main__":
    app = ToDoListApp()
    app.mainloop()
