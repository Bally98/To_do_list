import tkinter as tk
from tkinter import font
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
import sqlite3
from ttkthemes import ThemedTk, ThemedStyle


class App:
    def add_task(self):
        self.task = self.task_entry.get()
        if self.task:
            conn = sqlite3.connect("todo.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (task) VALUES (?)", (self.task,))
            conn.commit()
            conn.close()
            self.task_listbox.insert(tk.END, self.task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Empty field", "Please enter a task")

    def edit_task(self):
        self.selected_task_index = self.task_listbox.curselection()
        if self.selected_task_index:
            new_task = self.task_entry.get()
            if new_task:
                conn = sqlite3.connect("todo.db")
                cursor = conn.cursor()
                old_task = self.task_listbox.get(self.selected_task_index[0])
                cursor.execute("UPDATE tasks SET task=? WHERE task=?", (new_task, old_task))
                conn.commit()
                conn.close()
                self.task_listbox.delete(self.selected_task_index)
                self.task_listbox.insert(tk.END, new_task)
                self.task_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Empty field", "Please enter a new task value")
        else:
            messagebox.showwarning("Nothing selected", "Please select a task to edit")

    def delete_task(self):
        self.selected_task_index = self.task_listbox.curselection()
        if self.selected_task_index:
            conn = sqlite3.connect("todo.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task=?", (self.task_listbox.get(self.selected_task_index[0]),))
            conn.commit()
            conn.close()
            self.task_listbox.delete(self.selected_task_index)
        else:
            messagebox.showwarning("Nothing selected", "Please select a task to delete")

    def __init__(self, master):
        self.color = '#FFEFD5'
        self.defaultFont = font.nametofont("TkDefaultFont")

        self.defaultFont.configure(family="Terminal",
                                   size=14)
        self.title = Label(text='To Do list', background=self.color)
        self.title.pack(pady=20)

        text = ttk.Label(master, text="Write a task:", width=80, background=self.color)
        text.pack(fill='x', padx=60)

        self.task_entry = ttk.Entry(master, width=50, justify='left', font='Terminal')
        self.task_entry.pack(fill='x', padx=60)

        self.task_listbox = Listbox(master, width=60, bg='#F0FFF0', highlightcolor='black')
        self.task_listbox.pack(pady=7, fill='x', padx=30)

        self.add_button = ttk.Button(master, text="Add a task", command=self.add_task)
        self.add_button.pack(pady=7)

        self.edit_button = ttk.Button(master, text="Edit task", command=self.edit_task)
        self.edit_button.pack(pady=7)

        self.delete_button = ttk.Button(master, text="Delete task", command=self.delete_task)
        self.delete_button.pack(pady=7)


if __name__ == "__main__":
    root = Tk()
    root.title("To-Do List")
    root.geometry('600x700')
    root.config(background='#FFEFD5')
    photo = PhotoImage(file='todo4.png')
    root.iconphoto(False, photo)
    app = App(root)
    root.mainloop()
