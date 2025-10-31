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

        self.currententries = []

        self.currenttext = []



        self.manipulation_table = ctk.CTkFrame(self.mainframe, width=775, height=335)
        self.manipulation_table.pack(padx=0, pady=0, fill="both", expand=True)
        self.manipulation_table.place(x=20,y=5)

        logo_label = ctk.CTkLabel(self, image=long_logo, text="")

        logo_label.image = long_logo  # keep reference
        logo_label.place(x=750, y=0)  # adjust positioning

        self.loadbutton = ctk.CTkButton(self.mainframe, text="Create/Load Database", command=self.createTable)
        self.loadbutton.pack(pady=10)

        self.table_name_entry = ctk.CTkEntry(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.entry2 = ctk.CTkOptionMenu(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.entry3 = ctk.CTkOptionMenu(self.mainframe, width=100, height=20, font=("Helvetica", 14))
        self.table_name_entry.pack(pady=0)

        outer = ctk.CTkScrollableFrame(self.mainframe, width=375, height=500, orientation="vertical")
        outer.place(x=10, y=370)

        inner = ctk.CTkScrollableFrame(outer, width=375, height=500, orientation="horizontal")
        inner.pack(fill="both", expand=True)

        outer1 = ctk.CTkScrollableFrame(self.mainframe, width=375, height=500, orientation="vertical")
        outer1.place(x=405, y=370)

        inner1 = ctk.CTkScrollableFrame(outer1, width=375, height=500, orientation="horizontal")
        inner1.pack(fill="both", expand=True)

        self.tableframe = inner

        self.filterframe = inner1


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
                                      self.editcolumnbtn: self.editcolumn, self.addrowbtn: self.addrow, self.removerowbtn:
                                      self.removerow, self.editrowbtn: self.editrows
                                      }

        self.nocommand = (lambda *args, **kwargs: None)

        self.bind("<Left>", lambda e: inner._parent_canvas.xview_scroll(-5, "units"))
        self.bind("<Right>", lambda e: inner._parent_canvas.xview_scroll(5, "units"))
        self.bind("<Down>", lambda e: outer._parent_canvas.yview_scroll(5, "units"))
        self.bind("<Up>", lambda e: outer._parent_canvas.yview_scroll(-5, "units"))


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
        self.entry3.place_forget()
        for x in self.currententries:
            x.place_forget()
        for x in self.currenttext:
            x.place_forget()

        for widget in self.queryframe.winfo_children():
            widget.destroy()

        for i, query in enumerate(self.queries):
            entry = ctk.CTkEntry(self.queryframe, width=730)
            entry.bind("<Key>", lambda e: "break")
            entry.insert(0, query)
            entry.place(x=10, y=5 + i * 30)

        self.currententries.clear()
        self.currenttext.clear()


    def loadnewf(self):
        for x in self.all_manipulation_buttons:
            x.place_forget()
        self.loadbutton.pack(pady=10)
        self.table_name_entry.pack(pady=0)
        self.title("NoCodeSQL")
        self.table_title.configure(text="No Table Loaded")

        for widget in self.tableframe.winfo_children():
            widget.destroy()

        self.tableframe = ctk.CTkScrollableFrame(self.mainframe, width=375, height=530)
        self.tableframe.place(x=10, y=370)

        for widget in self.filterframe.winfo_children():
            widget.destroy()

        self.filterframe = ctk.CTkScrollableFrame(self.mainframe, width=375, height=530)
        self.filterframe.place(x=305, y=370)


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
            self.entry2.configure(values=["", "TEXT", "INTEGER", "REAL", "BLOB", "NUMERIC"],command=self.nocommand)
            self.text2.place(x=415, y=50)
            self.table_name_entry.place(x=285, y=80)
            self.entry2.set("")
            self.entry2.place(x=425, y=80)
        #REMOVE COLLUMN
        elif button == self.removecolumnbtn:
            columns = self.get_columns()
            self.text2.configure(text="Select Column:")
            self.text2.place(x=345, y=50)
            self.entry2.configure(values=columns,command=self.nocommand)
            self.entry2.set("")
            self.entry2.place(x=355, y=80)
        # EDIT COLUMN
        elif button == self.editcolumnbtn:
            columns = self.get_columns()
            self.text1.configure(text="New Name:")
            self.text1.place(x=410, y=50)
            self.text2.configure(text="Select Column:")
            self.text2.place(x=290, y=50)
            self.entry2.configure(values=columns,command=self.nocommand)
            self.entry2.set("")
            self.entry2.place(x=295, y=80)
            self.table_name_entry.place(x=415, y=79)
            self.table_name_entry.delete(0, ctk.END)
        # ADD ROW
        elif button == self.addrowbtn:
            columns = self.get_columns()
            done=0
            for x, col in enumerate(columns):
                if len(columns) > 8:
                    self.goback()
                    messagebox.showwarning("Column Error", "There are too many columns. Max=8")
                    break
                text = ctk.CTkLabel(self.manipulation_table, text=col)
                entry = ctk.CTkEntry(self.mainframe, width=100, height=20, font=("Helvetica", 14))
                self.currententries.append(entry)
                self.currenttext.append(text)
                text.place(x=175 + x * 120, y=40)
                entry.place(x=175 + x * 120, y=70)
                done = done + 1
                if done > 4:
                    entry.place(x=175 + (x-4) * 120, y=110)
                    text.place(x=175 + (x-4) * 120, y=80)
        # REMOVE ROW
        elif button == self.removerowbtn:
            columns = self.get_columns()
            self.entry2.set("")
            self.entry2.place(x=290, y=80)
            self.entry2.configure(values=columns, command=self.populatevalues)
            self.text1.place(x=285, y=50)
            self.text1.configure(text="Select Column:")
            self.entry3.place(x=410, y=80)
            self.entry3.set("")
            self.entry3.configure(values=["SELECT A COLUMN"])
            self.text2.place(x=405, y=50)
            self.text2.configure(text="Select Value:")
        # EDIT ROW
        elif button == self.editrowbtn:
            columns = self.get_columns()
            self.entry2.set("")
            self.entry2.place(x=355, y=45)
            self.entry2.configure(values=columns, command=self.populaterowvalues)






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
        self.currententries.clear()
        self.currenttext.clear()


    def block_click(self):
        return "break"

    def populaterowvalues(self, event=None):
        rows = self.populatevalues()
        done = 0
        for x, row in enumerate(rows):
            if len(rows) > 8:
                self.goback()
                messagebox.showwarning("Row Error", "There are too many rows. Max=8")
                break
            text = ctk.CTkLabel(self.manipulation_table, text=row)
            entry = ctk.CTkEntry(self.mainframe, width=100, height=20, font=("Helvetica", 14))
            self.currententries.append(entry)
            self.currenttext.append(text)
            text.place(x=198 + x * 120, y=46)
            entry.place(x=175 + x * 120, y=75)
            done = done + 1
            if done > 4:
                entry.place(x=175 + (x - 4) * 120, y=110)
                text.place(x=198 + (x - 4) * 120, y=85)

    ## SQL FUNCTIONS

    def editrows(self):
        key_column = self.entry2.get()  # column user selected
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        # Get all rows for that column
        cursor.execute(f'SELECT rowid, "{key_column}" FROM "{self.current_table}"')
        rows = cursor.fetchall()  # list of (rowid, value)

        for i, entry in enumerate(self.currententries):
            new_value = entry.get().strip()
            if new_value != "":
                rowid, original_value = rows[i]

                # Escape quotes if needed
                new_value_escaped = new_value.replace("'", "''")

                sql = f'UPDATE "{self.current_table}" SET "{key_column}" = \'{new_value_escaped}\' WHERE rowid = {rowid}'

                self.queries.append(sql)



        conn.close()
        self.loadTable()
        self.resetbuttons()

    def populatevalues(self, event=None):
        column = self.entry2.get()
        if not column or not getattr(self, "current_table", None):
            self.entry3.configure(values=[])
            return

        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        # fetch rowid + value (preserves order)
        cursor.execute(f'SELECT rowid, "{column}" FROM "{self.current_table}"')
        rows = cursor.fetchall()
        conn.close()

        # build display list and map to rowid
        display_list = []
        self._value_to_rowid = {}  # store on self for later lookup
        for rowid, val in rows:
            if val is None:
                display = f"{rowid}: <NULL>"
            else:
                display = f"{rowid}: {val}"
            display_list.append(display)
            self._value_to_rowid[display] = rowid

        if not display_list:
            display_list = ["<no values>"]

        self.entry3.configure(values=display_list)
        self.entry3.set(display_list[0])
        return display_list

    def addrow(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        columns = self.get_columns()

        values = [entry.get() for entry in self.currententries]

        for x in self.currententries:
            print(x)

        values = [v.strip() for v in values]

        formatted_values = []
        for v in values:
            if v == "":
                formatted_values.append("NULL")
            elif v.replace(".", "", 1).isdigit():  # integer or float
                formatted_values.append(v)
            else:
                # Escape internal quotes
                v = v.replace("'", "''")
                formatted_values.append(f"'{v}'")

        cols_sql = ", ".join([f'"{c}"' for c in columns])
        vals_sql = ", ".join(formatted_values)

        sql = f'INSERT INTO "{self.current_table}" ({cols_sql}) VALUES ({vals_sql});'
        print("SQL:", sql)

        self.queries.append(sql)

        self.loadTable()
        self.resetbuttons()

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

    def removerow(self):
        sel = self.entry3.get()
        if not sel:
            messagebox.showwarning("Selection", "No value selected.")
            return

        # lookup rowid
        rowid = self._value_to_rowid.get(sel)
        if rowid is None:
            messagebox.showerror("Lookup", "Could not map selection to a row.")
            return

        # append single SQL string (as you prefer)
        self.queries.append(f'DELETE FROM "{self.current_table}" WHERE rowid = {rowid}')

        # refresh UI
        self.loadTable()
        self.resetbuttons()

    def removecolumn(self):
        conn = sqlite3.connect(self.DB_FILE)
        cursor = conn.cursor()

        column_to_remove = self.entry2.get()

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

       self.table_title.configure(text=f"Database: {self.DB_FILE[50::]}")

       self.title(f"Database: {self.DB_FILE[50::]}")

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

       self.filterframe = self.tableframe

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
