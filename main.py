import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
from tkinter.simpledialog import askstring
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from soupsieve import select


class Main:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("750x750")
        self.root.title("Login Screen")
        self.root.resizable(False, False)
        
        self.bg = PhotoImage(file="images.png")
        self.bgLabel = Label(self.root, image=self.bg)
        self.bgLabel.place(x=0, y=0)

        self.WIDTH = self.root.winfo_screenwidth()
        self.HEIGHT = self.root.winfo_screenheight()

        self.connection = sqlite3.connect("database.db")
        self.connectionCursor = self.connection.cursor()

        self.connectionCursor.execute("""CREATE TABLE IF NOT EXISTS students (username string, password string)""")

        self.connection.commit()
        self.connection.close()

        Main.Front(self)


        self.root.mainloop()

    def Front(self):
        self.canvas = Canvas(self.root, bg="white", width=self.WIDTH / 3, height=self.HEIGHT / 2)
        self.canvas.place(x=50, y=100)

        self.loginLogo = PhotoImage(file=r"loginbutton.png", width=50, height=25)
        self.canvasBg = PhotoImage(file="images2.png")

        self.canvas.create_image(300, 320, image=self.canvasBg, anchor=NW)

        self.canvasColor = "white"

        self.emailLabel = Label(self.canvas, text="Your ID Number", bg=self.canvasColor)
        self.emailLabel.place(x=self.WIDTH / 7, y=self.HEIGHT / 8)
        self.emailEntry = ttk.Entry(self.canvas)
        self.emailEntry.place(x=self.WIDTH / 5, y=self.HEIGHT / 8)
        self.emailEntry.insert(0, "Enter Your ID Number Here!")

        self.passwordLabel = Label(self.canvas, text="Password", bg=self.canvasColor)
        self.passwordLabel.place(x=self.WIDTH / 7, y=self.HEIGHT / 6)
        self.passwordEntry = ttk.Entry(self.canvas, show="x")
        self.passwordEntry.place(x=self.WIDTH / 5, y=self.HEIGHT / 6)

        self.loginButton = ttk.Button(self.canvas, text="Login", image=self.loginLogo, compound=LEFT,
                                      command=lambda : Main.Login(self))
        self.loginButton.place(x=self.WIDTH / 4.8, y=self.HEIGHT / 5)

        self.registerLabel = Label(self.canvas, text = "You Don't Have Any Account?", bg=self.canvasColor)
        self.registerLabel.place(x=self.WIDTH / 5.8, y=self.HEIGHT / 4)
        self.registerButton = ttk.Button(self.canvas, text="Register", command=lambda : Main.Register(self))
        self.registerButton.place(x=self.WIDTH / 3.6, y=self.HEIGHT/4.05)

        self.deleteLabel = Label(self.canvas, text="Delete User", bg=self.canvasColor)
        self.deleteLabel.place(x=self.WIDTH / 100, y=self.HEIGHT / 2.3)

        self.deleteEntry = ttk.Entry(self.canvas)
        self.deleteEntry.place(x=self.WIDTH / 100, y=self.HEIGHT / 2.18)

        self.deleteButton = ttk.Button(self.canvas, text="Delete", command=lambda : Main.Delete(self))
        self.deleteButton.place(x=self.WIDTH / 10, y=self.HEIGHT / 2.2)

        self.treeView = ttk.Treeview(self.canvas, columns=('c1'), show='headings')
        self.treeView.place(x=self.WIDTH / 60, y=self.HEIGHT / 10)
        self.treeView.bind("<Double-1>", lambda x : Main.Selection(self))

        self.treeView.update()

        self.treeView.column("# 1", anchor=CENTER)
        self.treeView.heading("# 1", text="Registered List")

        self.treeViewLoader = sqlite3.connect("database.db")
        self.treeViewLoaderCursor = self.treeViewLoader.cursor()
        self.treeViewLoaderCursor.execute("SELECT username FROM students")
        self.datas = self.treeViewLoaderCursor.fetchall()

        self.treeView.insert("", 'end', values=(self.datas))

        self.treeViewLoader.commit()
        self.treeViewLoader.close()

    def Selection(self):
        self.select = self.treeView.focus()
        self.select = self.treeView.item(self.select, "values")
        self.selected = self.treeView.selection()
        self.deleteEntry.insert(0, self.select)

    def Delete(self):
        self.deleteTc = self.deleteEntry.get()
        self.deleteDb = sqlite3.connect("database.db")
        self.deleteDbCursor = self.deleteDb.cursor()
        self.deleteDbCursor.execute("DELETE FROM students WHERE username=?", (self.deleteTc,))
        self.treeView.delete(self.selected)
        self.deleteEntry.delete(0, END)
        
        self.deleteDb.commit()
        self.deleteDb.close()


    def Login(self):
        try:
            self.userName = self.emailEntry.get()
            self.password = self.passwordEntry.get()

            self.userName = int(self.userName)

            self.tuple = (self.userName, self.password)

            self.db = sqlite3.connect("database.db")
            self.dbcursor = self.db.cursor()

            self.dbcursor.execute("SELECT * FROM students")

            self.dataSet = self.dbcursor.fetchall()

            self.studentsList = []

            self.studentsList.append("")

            for data in self.dataSet:
                self.studentsList.append(data)

            for i in range(len(self.studentsList)):
                if self.tuple == self.studentsList[i]:
                    
                    self.url = "https://giris.turkiye.gov.tr/Giris/gir"
                    self.tarayici = webdriver.Chrome(executable_path="chromedriver");
                    self.tarayici.get(self.url)
            
                    self.tarayici.find_element_by_id("tridField").send_keys(str(self.userName))
                    # find password input field and insert password as well
                    self.tarayici.find_element_by_id("egpField").send_keys(str(self.password))
                    # click login button
                    self.tarayici.find_element_by_class_name("submitButton").click()
                    
                    break
                
                elif (i == (len(self.studentsList) - 1) and self.tuple != self.studentsList[i]):
                    showerror("Error!", "No such user found!")
                    
            self.studentsList.clear()

            self.db.close()
        
        except:
            showinfo("Error!", "Please Enter All Requiered Entry's.")

    def Register(self):

        self.id = askstring("ID", "Enter Your ID Here")
        self.passw = askstring("Password", "Enter Your Password Here", show="x")

        self.liste = [
            (self.id, self.passw)
        ]

        self.dataBase = sqlite3.connect("database.db")
        self.cursor = self.dataBase.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS students (username string, password string)""")

        self.cursor.executemany("insert into students values (?,?)", self.liste)

        self.treeView.insert("", 'end', values=(self.id))

        self.dataBase.commit()
        self.dataBase.close()
    


if __name__ == "__main__":
    Main()
