import sqlite3
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as msg


class MainFormClass:
    def mainFormLoad(self,firstName,lastName):
        self.firstName=firstName
        self.lastName=lastName
        mainForm = Tk()

        mainForm.title('MainForm')
        mainForm.geometry('850x300')
        right = int(mainForm.winfo_screenwidth() / 2 - 850 / 2)
        down = int(mainForm.winfo_screenheight() / 2 - 300 / 2)
        mainForm.geometry('+{}+{}'.format(right, down))
        mainForm.resizable(0, 0)
        mainForm.iconbitmap('images/MainForm.ico')



        def loadCustomerForm():
            mainForm.destroy()
            from CustomerForm import CustomerFormClass
            customerFormObject = CustomerFormClass()
            customerFormObject.customerFormLoad(self.firstName,self.lastName)




        lblWelcomeMesage = Label(mainForm, text=f'Welcome {firstName} {lastName}')
        lblWelcomeMesage.grid(row=0, column=0, padx=20, pady=20)



        customerImage = PhotoImage(file='images/customer.png')




        btnCustomer = Button(mainForm, text='Customer',image=customerImage,width=120,height=120,compound=TOP, command=loadCustomerForm,background="white")
        btnCustomer.grid(row=1, column=1, padx=20, pady=20)

        mainForm.mainloop()
