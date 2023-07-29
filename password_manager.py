import tkinter as tk
from tkinter import messagebox
import sqlite3
import tkinter.ttk as ttk

class PasswordManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")

        self.create_database()

        self.create_widgets()

    def create_database(self):
        conn = sqlite3.connect("passmanager.db")
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS manager (
                           app_name text,
                           url text,
                           email_id text,
                           password text
                        )""")

        conn.commit()
        conn.close()

    def create_widgets(self):
        self.app_name_entry = tk.Entry(self.root, width=30)
        self.app_name_entry.grid(row=0, column=1, padx=20)
        self.url_entry = tk.Entry(self.root, width=30)
        self.url_entry.grid(row=1, column=1, padx=20)
        self.email_id_entry = tk.Entry(self.root, width=30)
        self.email_id_entry.grid(row=2, column=1, padx=20)
        self.password_entry = tk.Entry(self.root, width=30)
        self.password_entry.grid(row=3, column=1, padx=20)

        tk.Label(self.root, text="Application Name:").grid(row=0, column=0)
        tk.Label(self.root, text="URL:").grid(row=1, column=0)
        tk.Label(self.root, text="Email Id:").grid(row=2, column=0)
        tk.Label(self.root, text="Password:").grid(row=3, column=0)

        tk.Button(self.root, text="Add Record", command=self.submit).grid(row=4, column=0, pady=5, padx=15, ipadx=35)

        tk.Button(self.root, text="Show Records", command=self.query).grid(row=4, column=1, pady=5, padx=5, ipadx=35)

        tk.Button(self.root, text="Delete Record", command=self.delete).grid(row=5, column=0, ipadx=30)

        tk.Button(self.root, text="Update Record", command=self.update).grid(row=5, column=1, ipadx=30)

        self.tree = ttk.Treeview(self.root, columns=("Application Name", "URL", "Email Id", "Password"), show="headings")
        self.tree.heading("Application Name", text="Application Name")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Email Id", text="Email Id")
        self.tree.heading("Password", text="Password")
        self.tree.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=6, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

    def submit(self):
        app_name = self.app_name_entry.get()
        url = self.url_entry.get()
        email_id = self.email_id_entry.get()
        password = self.password_entry.get()

        if app_name != "" and url != "" and email_id != "" and password != "":
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO manager VALUES (?, ?, ?, ?)", (app_name, url, email_id, password))

            conn.commit()
            conn.close()

            messagebox.showinfo("Info", "Record Added in Database!")

            self.app_name_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            self.email_id_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)

        else:
            messagebox.showinfo("Alert", "Please fill all details!")

    def query(self):
        conn = sqlite3.connect("passmanager.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM manager")
        records = cursor.fetchall()

        self.tree.delete(*self.tree.get_children())

        for record in records:
            self.tree.insert("", "end", values=record)

        conn.commit()
        conn.close()

    def delete(self):
        record_id = self.app_name_entry.get()
        if record_id != "":
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM manager WHERE app_name = ?", (record_id,))

            conn.commit()
            conn.close()

            messagebox.showinfo("Alert", f"Record with app_name '{record_id}' Deleted")

        else:
            messagebox.showinfo("Alert", "Please enter an application name to delete!")

    def update(self):
        record_id = self.app_name_entry.get()
        if record_id != "":
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM manager WHERE app_name = ?", (record_id,))
            record = cursor.fetchone()

            conn.close()

            if record:
                edit = tk.Toplevel(self.root)
                edit.title("Update Record")

                app_name_entry_edit = tk.Entry(edit, width=30)
                app_name_entry_edit.grid(row=0, column=1, padx=20)
                app_name_entry_edit.insert(0, record[0])
                url_entry_edit = tk.Entry(edit, width=30)
                url_entry_edit.grid(row=1, column=1, padx=20)
                url_entry_edit.insert(0, record[1])
                email_id_entry_edit = tk.Entry(edit, width=30)
                email_id_entry_edit.grid(row=2, column=1, padx=20)
                email_id_entry_edit.insert(0, record[2])
                password_entry_edit = tk.Entry(edit, width=30)
                password_entry_edit.grid(row=3, column=1, padx=20)
                password_entry_edit.insert(0, record[3])

                tk.Label(edit, text="Application Name:").grid(row=0, column=0)
                tk.Label(edit, text="URL:").grid(row=1, column=0)
                tk.Label(edit, text="Email Id:").grid(row=2, column=0)
                tk.Label(edit, text="Password:").grid(row=3, column=0)

                tk.Button(edit, text="Save Record", command=lambda: self.change(record[0], edit, app_name_entry_edit.get(), url_entry_edit.get(), email_id_entry_edit.get(), password_entry_edit.get())).grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

            else:
                messagebox.showinfo("Alert", f"Record with app_name '{record_id}' not found!")

        else:
            messagebox.showinfo("Alert", "Please enter an application name to update!")

    def change(self, old_app_name, edit_window, app_name, url, email_id, password):
        if app_name != "" and url != "" and email_id != "" and password != "":
            conn = sqlite3.connect("passmanager.db")
            cursor = conn.cursor()

            cursor.execute("""UPDATE manager SET 
                                app_name = ?,
                                url = ?,
                                email_id = ?,
                                password = ?
                                WHERE app_name = ?""",
                           (app_name, url, email_id, password, old_app_name))

            conn.commit()
            conn.close()

            messagebox.showinfo("Info", "Record Updated in Database!")

            edit_window.destroy()

            self.query()

        else:
            messagebox.showinfo("Alert", "Please fill all details!")

def main():
    root = tk.Tk()
    app = PasswordManagerApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
