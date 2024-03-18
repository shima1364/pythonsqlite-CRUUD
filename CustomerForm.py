import sqlite3
from tkinter import *
from tkinter import messagebox as msg
from tkinter import ttk



class CustomerFormClass:
    def customerFormLoad(self, firstName, lastName):
        #
        customerForm = Tk()

        customerForm.title('Customer Form')
        customerForm.geometry('1000x350')
        right = int(customerForm.winfo_screenwidth() / 2 - 1000 / 2)
        down = int(customerForm.winfo_screenheight() / 2 - 350 / 2)
        customerForm.geometry('+{}+{}'.format(right, down))
        customerForm.resizable(0, 0)
        customerForm.columnconfigure(index=0, weight=2)
        customerForm.columnconfigure(index=1, weight=2)
        customerForm.columnconfigure(index=2, weight=4)

        customerForm.rowconfigure(index=0, weight=4)
        customerForm.rowconfigure(index=1, weight=1)
        customerForm.rowconfigure(index=2, weight=1)

        def backMainForm():
            customerForm.destroy()
            from MainForm import MainFormClass
            mainFormObject = MainFormClass()
            mainFormObject.mainFormLoad(firstName, lastName)

        def search(*args):
            tvDataBase.delete(*tvDataBase.get_children())

            connectionString = 'DB/BookStore.db'
            if txtSearchFieldEntry == "":
                showList()
            if txtSearchFieldComboBox.get() == "All Fields":
                commandText = (f"SELECT * FROM Customers WHERE ID LIKE '%{txtSearchFieldEntry.get()}%'"
                               f" OR FirstName  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR LastName  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR Mobile  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR NationalCode  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR City  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR Zipcode  LIKE '%{txtSearchFieldEntry.get()}%'"
                               f"OR Email  LIKE '%{txtSearchFieldEntry.get()}%'")
            else:
                commandText = (
                    f"SELECT * FROM Customers WHERE {txtSearchFieldComboBox.get()} LIKE '%{txtSearchFieldEntry.get()}%'")

            showList(commandText)
            # with sqlite3.Connection(connectionString) as connection:
            #     cursor = connection.cursor()
            #     cursor.execute(commandText, )
            #     rows = cursor.fetchall()
            #     for row in rows:
            #         values = []
            #         for value in row:
            #             if value == None:
            #                 values.append("")
            #             else:
            #                 values.append(value)
            #
            #         tvDataBase.insert("", "end", values=values)

        def showList(commandText='select * from Customers', *args):
            tvDataBase.delete(*tvDataBase.get_children())

            connectionString = 'DB/BookStore.db'
            # commandText = 'select * from Customers'
            with sqlite3.Connection(connectionString) as connection:
                cursor = connection.cursor()
                cursor.execute(commandText, )
                rows = cursor.fetchall()
                rowCount = 0
                for row in rows:
                    rowCount += 1
                    values = [rowCount]
                    for value in row:
                        if value == None:
                            values.append("")
                        else:
                            values.append(value)

                    tvDataBase.insert("", "end", values=values)

        def ClearForm():
            txtCustomerID.set("")
            widgets = frmInfo.winfo_children()
            # widgets.extend(frmButton.winfo_children())

            for widget in widgets:
                if isinstance(widget, Entry):
                    widget.delete(0, "end")

        def addCustomer():
            connectionString = 'DB/BookStore.db'
            commandText = (
                'INSERT INTO Customers(FirstName,LastName,Mobile,NationalCode,City,Zipcode,Email) VALUES (?,?,?,?,?,?,?)')

            values = (txtFirstName.get(), txtLastName.get(), txtMobile.get(), txtNationalCode.get(), txtCity.get(),
                      txtZipcode.get(), txtEmail.get())
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
                # message=str(error.args[0]).split(".")[-1]
                msg.showerror("Error", message=error.args[0])
            showList()

        def deleteCustomer():
            connectionString = 'DB/BookStore.db'
            commandText = f"DELETE FROM Customers WHERE ID IS {txtCustomerID.get()} "

            try:
                with sqlite3.Connection(connectionString) as connection:
                    cursor = connection.cursor()
                    cursor.execute("PRAGMA foreign_keys = '1'")
                    cursor.execute(commandText)
                    connection.commit()
            except Exception as error:
                # message=str(error.args[0]).split(".")[-1]
                msg.showerror("Error", message=error.args[0])
            showList()

        def editCustomer():
            connectionString = 'DB/BookStore.db'

            values = (txtFirstName.get(), txtLastName.get(), txtMobile.get(),
                      txtNationalCode.get(), txtCity.get(), txtZipcode.get(), txtEmail.get(), txtCustomerID.get())
            params = []
            for value in values:
                if value == "":
                    params.append(None)
                else:
                    params.append(value)
            commandText = f"UPDATE Customers SET FirstName =?,LastName =?, Mobile =?,NationalCode=?, City = ?, Zipcode = ?, Email = ? WHERE ID IS ?"
            try:
                with sqlite3.Connection(connectionString) as connection:
                    cursor = connection.cursor()
                    cursor.execute("PRAGMA foreign_keys = '1'")
                    cursor.execute(commandText, params)
                    connection.commit()
            except Exception as error:
                # message=str(error.args[0]).split(".")[-1]
                msg.showerror("Error", message=error.args[0])
            showList()

        def onTreeSelect(event):
            ClearForm()
            index = tvDataBase.selection()
            if index:
                selectedValues = tvDataBase.item(index)#["values"]
                txtFirstName.set(selectedValues[2])
                txtLastName.set(selectedValues[3])
                txtMobile.set(selectedValues[4])
                txtNationalCode.set(selectedValues[5])
                txtCity.set(selectedValues[6])
                txtZipcode.set(selectedValues[7])
                txtEmail.set(selectedValues[8])
                txtCustomerID.set(selectedValues[1])

        def checkNationalCodeValidation(*args):

            if not txtNationalCode.get().isnumeric():
                result = txtNationalCode.get()
                for c in result:
                    if not c.isnumeric():
                        result = result.replace(c, '')

                # txtNationalCode.set(txtNationalCode.get()[:len(txtNationalCode.get()) - 1])
                txtNationalCode.set(result)
            if len(txtNationalCode.get()) > 10:
                txtNationalCode.set(txtNationalCode.get()[:len(txtNationalCode.get()) - 1])

        def checkMobileValidation(*args):

            if not txtMobile.get().isnumeric():
                result = txtMobile.get()
                for c in result:
                    if not c.isnumeric():
                        result = result.replace(c, '')

                # txtNationalCode.set(txtNationalCode.get()[:len(txtNationalCode.get()) - 1])
                txtMobile.set(result)
            if len(txtMobile.get()) > 11:
                txtMobile.set(txtMobile.get()[:len(txtMobile.get()) - 1])

        def checkZipcodeValidation(*args):

            if not txtZipcode.get().isnumeric():
                result = txtZipcode.get()
                for c in result:
                    if not c.isnumeric():
                        result = result.replace(c, '')

                # txtNationalCode.set(txtNationalCode.get()[:len(txtNationalCode.get()) - 1])
                txtZipcode.set(result)
            if len(txtZipcode.get()) > 10:
                txtZipcode.set(txtZipcode.get()[:len(txtZipcode.get()) - 1])

        def checkFirstNameValidation(*args):
            result = txtFirstName.get()

            if not result.isalpha():

                for c in result:

                    if not c.isalpha():
                        result = result.replace(c, '')
            txtFirstName.set(result)

        def checkLastNameValidation(*args):
            result = txtLastName.get()

            if not result.isalpha():

                for c in result:

                    if not c.isalpha():
                        result = result.replace(c, '')
            txtLastName.set(result)

        frmInfo = ttk.Frame(customerForm, height=400)
        frmInfo.grid(row=0, column=0, rowspan=10, padx=3, pady=3, ipadx=5, ipady=5, sticky="nsew", )

        lblCustumerId = ttk.Label(frmInfo, text="Customer ID")
        lblCustumerId.grid(row=0, column=0, padx=10, pady=2, sticky="w")

        txtCustomerID = StringVar()
        lblCustumerIdValue = ttk.Label(frmInfo, textvariable=txtCustomerID)
        lblCustumerIdValue.grid(row=0, column=1, padx=10, pady=2, sticky="w")
        lblFirstName = ttk.Label(frmInfo, text="First Name")
        lblFirstName.grid(row=1, column=0, padx=10, pady=2, sticky="w")
        txtFirstName = StringVar()
        txtFirstName.trace("w", checkFirstNameValidation)
        entFirstName = ttk.Entry(frmInfo, textvariable=txtFirstName)
        entFirstName.grid(row=1, column=1, padx=10, pady=2, sticky="ew")

        lblLastName = ttk.Label(frmInfo, text="Last Name")
        lblLastName.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        txtLastName = StringVar()
        txtLastName.trace("w", checkLastNameValidation)
        entLastName = ttk.Entry(frmInfo, textvariable=txtLastName)
        entLastName.grid(row=2, column=1, padx=10, pady=2, sticky="ew")

        lblMobile = ttk.Label(frmInfo, text="Mobile")
        lblMobile.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        txtMobile = StringVar()
        txtMobile.trace("w", checkMobileValidation)
        entMobile = ttk.Entry(frmInfo, textvariable=txtMobile)
        entMobile.grid(row=3, column=1, padx=10, pady=2, sticky="ew")

        lblNationalCode = ttk.Label(frmInfo, text="NationalCode")
        lblNationalCode.grid(row=4, column=0, padx=10, pady=2, sticky="w")
        txtNationalCode = StringVar()
        txtNationalCode.trace("w", checkNationalCodeValidation)
        entNationalCode = ttk.Entry(frmInfo, textvariable=txtNationalCode)
        entNationalCode.grid(row=4, column=1, padx=10, pady=2, sticky="ew")

        lblZipcode = ttk.Label(frmInfo, text="Zipcode")
        lblZipcode.grid(row=5, column=0, padx=10, pady=2, sticky="w")
        txtZipcode = StringVar()
        txtZipcode.trace('w', checkZipcodeValidation)
        entZipcode = ttk.Entry(frmInfo, textvariable=txtZipcode)
        entZipcode.grid(row=5, column=1, padx=10, pady=2, sticky="ew")

        lblCity = ttk.Label(frmInfo, text="City")
        lblCity.grid(row=6, column=0, padx=10, pady=2, sticky="w")
        txtCity = StringVar()
        entCity = ttk.Entry(frmInfo, textvariable=txtCity)
        entCity.grid(row=6, column=1, padx=10, pady=2, sticky="ew")

        lblEmail = ttk.Label(frmInfo, text="Email")
        lblEmail.grid(row=7, column=0, padx=10, pady=2, sticky="w")
        txtEmail = StringVar()
        entEmail = ttk.Entry(frmInfo, textvariable=txtEmail)
        entEmail.grid(row=7, column=1, padx=10, pady=2, sticky="ew")

        lblImformation = ttk.Label(frmInfo, text="Fill the fields to add or change customer settings")
        lblImformation.grid(row=8, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        frmTreeView = ttk.Frame(customerForm, relief="solid", borderwidth=3)
        frmTreeView.columnconfigure(index=0, weight=1)
        frmTreeView.rowconfigure(index=0, weight=1)
        frmTreeView.grid(row=0, column=2, rowspan=4, columnspan=4, padx=2, pady=2, ipadx=5, ipady=5, sticky="nsew")
        style = ttk.Style()
        style.configure("my.Treeview", font=("arial", 8), background="white", foreground="black")

        tvColumns = ["Index", "Customer ID", "FirstName", "LastName", "Mobile", "NationalCode", "City", "Zipcode",
                     "Email"]
        displayColumns = ["Index", "FirstName", "LastName", "Mobile", "NationalCode", "City", "Zipcode", "Email"]
        tvDataBase = ttk.Treeview(frmTreeView, columns=tvColumns, style="my.Treeview", selectmode="browse",
                                  show="headings", displaycolumns=displayColumns)
        tvDataBase.grid(row=0, column=0, padx=0, pady=0, sticky=NSEW, )
        tvDataBase.bind("<<TreeviewSelect>>", onTreeSelect)

        tvDataBase.column("#0", width=0)
        tvDataBase.column("Index", width=20)
        tvDataBase.heading("Index", text="#", anchor="w")

        tvDataBase.column("Customer ID", width=0)
        tvDataBase.heading("Customer ID", text="CustomerID")

        tvDataBase.column("FirstName", width=100)
        tvDataBase.heading("FirstName", text="FirstName", anchor="w")

        tvDataBase.column("LastName", width=90)
        tvDataBase.heading("LastName", text="LastName", anchor="w")

        tvDataBase.column("Mobile", width=90)
        tvDataBase.heading("Mobile", text="Mobile", anchor="w")

        tvDataBase.column("NationalCode", width=90)
        tvDataBase.heading("NationalCode", text="NationalCode", anchor="w")

        tvDataBase.column("City", width=75)
        tvDataBase.heading("City", text="City", anchor="w")

        tvDataBase.column("Zipcode", width=80)
        tvDataBase.heading("Zipcode", text="Zipcode", anchor="w")

        tvDataBase.column("Email", width=150)
        tvDataBase.heading("Email", text="Email", anchor="w")

        frmButton = ttk.Frame(customerForm)
        frmButton.grid(row=5, columnspan=5, rowspan=2, padx=10, pady=10, sticky="ew")
        btnAddCustomer = ttk.Button(frmButton, text="Add Customer", command=addCustomer, width=20)
        btnAddCustomer.grid(row=0, column=0, padx=10, pady=2, sticky="ew")
        btnEditCustomer = ttk.Button(frmButton, text="Edit Customer", command=editCustomer, width=20)
        btnEditCustomer.grid(row=0, column=1, padx=10, pady=2, sticky="ew")
        btnDeleteCustomer = ttk.Button(frmButton, text="Delete Customer", command=deleteCustomer, width=20)
        btnDeleteCustomer.grid(row=1, column=0, padx=10, pady=2, sticky="ew")
        btnClearForm = ttk.Button(frmButton, text="Clear Form", command=ClearForm, width=20)
        btnClearForm.grid(row=1, column=1, padx=10, pady=2, sticky="ew")

        lblSearchDataBase = Label(frmButton, text="Search")
        lblSearchDataBase.grid(row=0, column=3, padx=10, pady=10, sticky="e")

        searchFieldList = ["All Fields", "FirstName", "LastName", "Mobile", "NationalCode", "City", "Zipcode", "Email"]
        txtSearchFieldComboBox = StringVar()
        txtSearchFieldComboBox.set(searchFieldList[0])

        cbSearchField = ttk.Combobox(frmButton, values=searchFieldList, textvariable=txtSearchFieldComboBox,
                                     state="readonly", width=10, xscrollcommand=search)
        cbSearchField.grid(row=0, column=4, padx=10, pady=10, sticky="e")

        txtSearchFieldEntry = StringVar()
        txtSearchFieldEntry.trace("w", search)

        entSearchField = ttk.Entry(frmButton, textvariable=txtSearchFieldEntry)
        entSearchField.grid(row=0, column=5, padx=10, pady=10, sticky="e")

        btnBack = ttk.Button(customerForm, text="MainForm", command=backMainForm)
        btnBack.grid(row=6, column=5, padx=10, pady=10, sticky="w")

        showList()
        customerForm.mainloop()

customerFormObject = CustomerFormClass()
customerFormObject.customerFormLoad('Vahid','Ghorbani')
