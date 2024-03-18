import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox as msg

class SampleFormClass:
    def __init__(self):
        pass

    def sampleFormClass_Load(self):
        employeeFormObject = Tk()
        employeeFormObject.title('Employee Form')
        employeeFormObject.geometry('800x400')
        x = int(employeeFormObject.winfo_screenwidth()/2  - 800/2)
        y = int(employeeFormObject.winfo_screenheight()/2 - 400/2)
        employeeFormObject.geometry('+{}+{}'.format(x,y))


        def clearForm():
            pass

        def onTreeSelect(event):
            clearForm()
            index = tvDataBase.selection()
            if index:
                selectedValues = tvDataBase.item(index)["values"]
                txtFirstName.set(selectedValues[2])
                txtLastName.set(selectedValues[3])
                txtNationalCode.set(selectedValues[4])

        def showList(*args):
            tvDataBase.delete(*tvDataBase.get_children())
            connectionString = 'DB/BookStore.db'
            commandText = 'select * from employee'
            with sqlite3.Connection(connectionString) as connection:
                cursor = connection.cursor()
                cursor.execute(commandText, )
                rows = cursor.fetchall()
            rowCount = 0
            for row in rows:
                rowCount +=1
                valuesOfRow = [rowCount]
                for value in row:
                    if value is None:
                        valuesOfRow.append("")
                    else:
                        valuesOfRow.append(value)
                tvDataBase.insert("","end",values=valuesOfRow)

        def addCustomer():
            connectionString = 'DB/BookStore.db'
            commandText = (
                'INSERT INTO employee(FirstName,LastName,NationalCode) VALUES (?,?,?)')

            values = (txtFirstName.get(), txtLastName.get(),txtNationalCode.get())
            params = []
            for value in values:
                if value == "":

                    params.append(None)
                else:
                    params.append(value)
            try:
                with sqlite3.Connection(connectionString) as connection:
                    cursor = connection.cursor()
                    cursor.execute("PRAGMA foreign_keys = '1'")
                    cursor.execute(commandText, params)
                    connection.commit()
            except Exception as error:
                msg.showerror("Error", message=error.args[0])
            showList()

        lblFirstName = Label(employeeFormObject,text='FirstName: ')
        lblFirstName.grid(padx=10,pady=10,row=0,column=0,sticky='w')

        txtFirstName=StringVar()
        entFirstName = ttk.Entry(employeeFormObject,width=40,textvariable=txtFirstName)
        entFirstName.grid(padx=10,pady=10,row=0,column=1,sticky='w')

        lblLastName = Label(employeeFormObject, text='LastName: ')
        lblLastName.grid(padx=10, pady=10, row=1, column=0, sticky='w')

        txtLastName = StringVar()
        entLastName = ttk.Entry(employeeFormObject, width=40, textvariable=txtLastName)
        entLastName.grid(padx=10, pady=10, row=1, column=1, sticky='w')

        lblNationalCode = Label(employeeFormObject, text='NationalCode: ')
        lblNationalCode.grid(padx=10, pady=10, row=2, column=0, sticky='w')

        txtNationalCode = StringVar()
        entNationalCode = ttk.Entry(employeeFormObject, width=40, textvariable=txtNationalCode)
        entNationalCode.grid(padx=10, pady=10, row=2, column=1, sticky='w')

        btnRegister = ttk.Button(employeeFormObject,width=10,text='Insert',command=addCustomer)
        btnRegister.grid(row=3,column=1,padx=10,pady=20,sticky='w')

        btnRegister = ttk.Button(employeeFormObject,width=10,text='Update')
        btnRegister.grid(row=3,column=1,padx=10,pady=20)

        btnRegister = ttk.Button(employeeFormObject,width=10,text='Delete')
        btnRegister.grid(row=3,column=1,padx=10,pady=20,sticky='e')



        frmTreeView = ttk.Frame(employeeFormObject,borderwidth=3)
        frmTreeView.columnconfigure(index=0, weight=1)
        frmTreeView.rowconfigure(index=0, weight=1)
        frmTreeView.grid(row=0,column=2,columnspan=4,rowspan=4,padx=2,pady=2)

        tvColumns = ["Index", "ID", "FirstName", "LastName", "NationalCode"]
        displayColumns = ["Index", "FirstName", "LastName", "NationalCode"]

        tvDataBase = ttk.Treeview(frmTreeView,  show="headings",selectmode="browse", columns=tvColumns, displaycolumns=displayColumns)
        tvDataBase.grid(row=0, column=0, padx=0, pady=0,ipadx=5, ipady=5, sticky=NSEW )

        tvDataBase.bind("<<TreeviewSelect>>", onTreeSelect)

        tvDataBase.column("#0", width=0)
        tvDataBase.column("Index", width=20,anchor='n')
        tvDataBase.heading("Index", text="#", anchor="n")

        tvDataBase.column("ID", width=0)
        tvDataBase.heading("ID", text="ID")

        tvDataBase.column("FirstName", width=100)
        tvDataBase.heading("FirstName", text="FirstName", anchor="n")

        tvDataBase.column("LastName", width=90)
        tvDataBase.heading("LastName", text="LastName", anchor="n")

        tvDataBase.column("NationalCode", width=120)
        tvDataBase.heading("NationalCode", text="NationalCode", anchor="n")


        showList()
        employeeFormObject.mainloop()



sampleFormObject = SampleFormClass()
sampleFormObject.sampleFormClass_Load()