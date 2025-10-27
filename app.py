#NOCODESQL main app file
import customtkinter as ctk
import sqlite3
import os
from tkinter import messagebox, filedialog
from PIL import Image
from functools import partial
import shutil

data_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(data_dir, "data")


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):


    def __init__(self):
        super().__init__()
        self.title("NoCodeSQL")
        self.geometry("850x975")
        self.configure(bg="#0F0F0F")
        self.resizable(False, False)
        self.iconbitmap("resources/logo.ico")

        self.DB_FILE = os.path.join(data_folder, "")

        self.mainframe = ctk.CTkFrame(self, width=800, height=900)
        self.mainframe.pack(padx=20, pady=30, fill="both", expand=True)

        long_logo = ctk.CTkImage(
            light_image=Image.open("resources/titlelogo.png"),
            dark_image=Image.open("resources/titlelogo.png"),
            size=(80,18)
        )

        self.queries = []



        self.manipulation_table = ctk.CTkFrame(self.mainframe, width=775, height=335)
        self.manipulation_table.pack(padx=0, pady=0, fill="both", expand=True)
        self.manipulation_table.place(x=20,y=5)

        logo_label = ctk.CTkLabel(self, image=long_logo, text="")

        logo_label.image = long_logo  # keep reference
        logo_label.place(x=750, y=0)  # adjust positioning

        self.loadbutton = ctk.CTkButton(self.mainframe, text="Create/Load Table", command=self.createTable)
        self.loadbutton.pack(pady=10)

        self.table_name_entry = ctk.CTkEntry(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.entry2 = ctk.CTkOptionMenu(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.entry3 = ctk.CTkOptionMenu(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.table_name_entry.pack(pady=0)


        self.tableframe = ctk.CTkFrame(self.mainframe, width=775, height=550)
        self.tableframe.place(x=20,y=370)

        self.run_query = ctk.CTkButton(self, text="Run Query", state="normal", height=40, width=160, command=self.runquery)
        self.run_query.place(x=345,y=300)

        self.queryframe = ctk.CTkFrame(self.manipulation_table, width=755, height=115)
        self.queryframe.place(relx=0.5,y=185, anchor="center")

        self.table_title = ctk.CTkButton(self, text="No Table Loaded", state="normal", height=20, width=80)
        self.table_title.place(relx=0.5,y=384, anchor="center")

        self.text1 = ctk.CTkLabel(self.manipulation_table, text="ERROR:")
        self.text2 = ctk.CTkLabel(self.manipulation_table, text="ERROR:")
        self.text3 = ctk.CTkLabel(self.manipulation_table, text="ERROR:")

        self.table_title.bind("<Button-1>", self.block_click())

        self.backbtn = ctk.CTkButton(self.manipulation_table, text="Go Back", command=self.goback)

        self.addcolumnbtn = ctk.CTkButton(self.manipulation_table, text="Add Column")
        self.removecolumnbtn = ctk.CTkButton(self.manipulation_table, text="Remove Column")
        self.editcolumnbtn = ctk.CTkButton(self.manipulation_table, text="Edit Column")

        self.addrowbtn = ctk.CTkButton(self.manipulation_table, text="Add Row")
        self.removerowbtn = ctk.CTkButton(self.manipulation_table, text="Remove Row")
        self.editrowbtn = ctk.CTkButton(self.manipulation_table, text="Edit Row")

        self.selectbtn = ctk.CTkButton(self.manipulation_table, text="Select")
        self.filterbtn = ctk.CTkButton(self.manipulation_table, text="Where")
        self.joinbtn = ctk.CTkButton(self.manipulation_table, text="Join")

        self.orderbybtn = ctk.CTkButton(self.manipulation_table, text="Order By")
        self.groupbybtn = ctk.CTkButton(self.manipulation_table, text="Group By")
        self.aggregatebtn = ctk.CTkButton(self.manipulation_table, text="Aggregate")

        self.loadnew= ctk.CTkButton(self.manipulation_table, text="Load New")
        self.exportbtn = ctk.CTkButton(self.manipulation_table, text="Export")
        self.clearqrybtn = ctk.CTkButton(self.manipulation_table, text="Clear Query")

        self.all_manipulation_buttons = {self.addcolumnbtn, self.removecolumnbtn, self.editcolumnbtn,
                                         self.addrowbtn, self.removerowbtn, self.editrowbtn, self.selectbtn,
                                         self.filterbtn, self.joinbtn, self.orderbybtn, self.groupbybtn,
                                         self.aggregatebtn, self.exportbtn, self.loadnew, self.clearqrybtn
                                         }

        self.resetbuttons()

        self.manipulation_commands = {self.addcolumnbtn: self.addcolumn, self.removecolumnbtn: self.removecolumn,
                                      self.editcolumnbtn: self.editcolumn
                                      }


        logo_label.lift()

    ## GUI FUNCTIONS

    def resetbuttons(self):
        for x in self.all_manipulation_buttons:
            if x == self.clearqrybtn:
                x.configure(command=self.clearquery)
            elif x == self.exportbtn:
                x.configure(command=self.export)
            elif x == self.loadnew:
                x.configure(command=self.loadnewf)
            else:
                x.configure(command=partial(self.pick, x))
        self.backbtn.place_forget()
        self.text1.place_forget()
        self.text2.place_forget()
        self.table_name_entry.place_forget()
        self.entry2.place_forget()

        for widget in self.queryframe.winfo_children():
            widget.destroy()

        for i, query in enumerate(self.queries):
            entry = ctk.CTkEntry(self.queryframe, width=730)
            entry.bind("<Key>", lambda e: "break")
            entry.insert(0, query)
            entry.place(x=10, y=5 + i * 30)


    def loadnewf(self):
        for x in self.all_manipulation_buttons:
            x.place_forget()
        self.loadbutton.pack(pady=10)
        self.table_name_entry.pack(pady=0)
        self.title("NoCodeSQL")
        self.table_title.configure(text="No Table Loaded")

        for widget in self.tableframe.winfo_children():
            widget.destroy()

        self.tableframe = ctk.CTkScrollableFrame(self.mainframe, width=775, height=550)
        self.tableframe.place(x=20, y=370)


    def goback(self):
        self.manipulateTable()
        self.resetbuttons()


    def pick(self, button):
        for x in self.all_manipulation_buttons:
            x.place_forget()
        button.place(x=315,y=10)
        self.backbtn.place(x=20,y=10)
        #ADD COLUMN
        if button == self.addcolumnbtn:
            self.table_name_entry.delete(0, ctk.END)
            self.text1.configure(text="Column Name:")
            self.text1.place(x=275, y=50)
            self.text2.configure(text="Column Type:")
            self.entry2.configure(values=["", "TEXT", "INTEGER", "REAL", "BLOB", "NUMERIC"])
            self.text2.place(x=415, y=50)
            self.table_name_entry.place(x=285, y=80)
            self.entry2.set("")
            self.entry2.place(x=425, y=80)
        #REMOVE COLLUMN
        elif button == self.removecolumnbtn:
            columns = self.get_columns()
            self.text2.configure(text="Select Column:")
            self.text2.place(x=345, y=50)
            self.entry2.configure(values=columns)
            self.entry2.set("")
            self.entry2.place(x=355, y=80)
        elif button == self.editcolumnbtn:
            columns = self.get_columns()
            self.text1.configure(text="New Name:")
            self.text1.place(x=410, y=50)
            self.text2.configure(text="Select Column:")
            self.text2.place(x=290, y=50)
            self.entry2.configure(values=columns)
            self.entry2.set("")
            self.entry2.place(x=295, y=80)
            self.table_name_entry.place(x=415, y=79)
            self.table_name_entry.delete(0, ctk.END)
        if button in self.manipulation_commands:
            button.configure(command=self.manipulation_commands[button])

    def manipulateTable(self):
        self.loadbutton.forget()
        self.table_name_entry.forget()

        self.table_name_entry.delete(0, ctk.END)

        self.loadnew.place(x=615,y=15)
        self.exportbtn.place(x=615,y=50)
        self.clearqrybtn.place(x=615,y=85)

        self.orderbybtn.place(x=465, y=15)
        self.groupbybtn.place(x=465, y=50)
        self.aggregatebtn.place(x=465, y=85)

        self.selectbtn.place(x=315, y=15)
        self.filterbtn.place(x=315, y=50)
        self.joinbtn.place(x=315, y=85)

        self.addrowbtn.place(x=165, y=15)
        self.removerowbtn.place(x=165, y=50)
        self.editrowbtn.place(x=165, y=85)

        self.addcolumnbtn.place(x=15, y=15)
        self.removecolumnbtn.place(x=15, y=50)
        self.editcolumnbtn.place(x=15, y=85)

    def clearquery(self):
        self.queries.clear()
        self.resetbuttons()


    def block_click(self):
        return "break"


    ## SQL FUNCTIONS

    def export(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".db",
            filetypes=[("SQLite Database", "*.db")],
            initialfile=os.path.basename(self.DB_FILE)
        )

        if not save_path:
            return

        shutil.copy(self.DB_FILE, save_path)

    def editcolumn(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        column_to_edit = self.entry2.get()
        column_new_name = self.table_name_entry.get()

        if column_to_edit != "":
            if column_new_name != "":
                self.queries.append(f"ALTER TABLE {self.current_table} RENAME COLUMN {column_to_edit} TO {column_new_name}")

        conn.close()

        self.loadTable()
        self.resetbuttons()



    def removecolumn(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        column_to_remove = self.entry2.get()

        print(column_to_remove)

        cursor.execute(f"PRAGMA table_info({self.current_table})")
        columns = cursor.fetchall()

        keep = [c[1] for c in columns if c[1] != column_to_remove]

        self.queries.append(f"CREATE TABLE temp_table AS SELECT {', '.join(keep)} FROM {self.current_table}")
        self.queries.append(f"DROP TABLE {self.current_table}")
        self.queries.append(f"ALTER TABLE temp_table RENAME TO {self.current_table}")

        conn.close()

        self.loadTable()
        self.resetbuttons()


    def get_columns(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({self.current_table})")
        columns = cursor.fetchall()

        column_names = [col[1] for col in columns]
        conn.close()

        return column_names

    def runquery(self):
        if self.queries == []:
            messagebox.showwarning("Query Error", "There are no queries to run.")
            return

        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        for x in self.queries:
            cursor.execute(x)
            print("hi")

        conn.commit()
        conn.close()

        self.queries.clear()
        self.loadTable()
        self.resetbuttons()


    def addcolumn(self):
        name = self.table_name_entry.get().strip()
        type = self.entry2.get().strip()
        table_name = self.current_table


        sql = f"ALTER TABLE {table_name} ADD COLUMN {name} {type}"
        self.queries.append(sql)

        self.goback()

    def loadTable(self):

       self.table_title.configure(text=f"Table: {self.DB_FILE[50::]}")

       self.title(f"Table: {self.DB_FILE[50::]}")

       # Clear previous widgets
       for widget in self.tableframe.winfo_children():
           widget.destroy()

       if not os.path.exists(self.DB_FILE):
           return

       conn = sqlite3.connect(self.DB_FILE)
       cursor = conn.cursor()

       try:
           cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
           table_name = cursor.fetchone()
           if table_name is None:
               conn.close()
               return
           table_name = table_name[0]

           self.current_table = table_name

           cursor.execute(f"PRAGMA table_info({table_name})")
           columns_info = cursor.fetchall()
           column_names = [col[1] for col in columns_info]

           cursor.execute(f"SELECT * FROM {table_name}")
           rows = cursor.fetchall()
       except sqlite3.OperationalError:
           conn.close()
           return

       conn.close()

       for col, text in enumerate(column_names):
           label = ctk.CTkLabel(self.tableframe, text=text, font=("Helvetica", 12, "bold"))
           label.grid(row=0, column=col, padx=2, pady=0)

       for r, row in enumerate(rows, start=1):
           for c, value in enumerate(row):
               label = ctk.CTkLabel(self.tableframe, text=str(value))
               label.grid(row=r, column=c, padx=20, pady=0)

       self.manipulateTable()

    def createTable(self):
        table_name = self.table_name_entry.get()

        if  table_name.strip() == "":
            messagebox.showwarning("Input Error", "Table Name cannot be empty!")
            return
        self.DB_FILE = os.path.join(data_folder, table_name + ".db")

        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS generic_table (
            column1 TEXT
        )
        """)


        conn.commit()
        conn.close()

        self.loadTable()


if __name__ == "__main__":
    app = App()
    app.mainloop()
