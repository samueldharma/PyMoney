from email import message
from tkinter import messagebox
from turtle import width
import pyrecord
import pycategory
records = pyrecord.Records()
categories = pycategory.Categories()


from tkinter import *
from tkinter import ttk
from tkcalendar import *
from datetime import date
d = date.today()

root = Tk()
root.title('MyPymoney')

record = [0, '', 0, 0]
balance = 0

def find():
    for item in recordsTree.get_children():recordsTree.delete(item)
    _find = findEntry.get()
    if len(_find.split('-')) == 2:
        filtered = records.find(_find)
    else:
        target_categories = categories.find_subcategories(_find, categories._categories)
        filtered = records.find(target_categories)
    number = 1
    total_expense_income = 0
    if filtered != []:
        for date, category, desc, amount in filtered:
            recordsTree.insert('', 'end', text = str(number), values=(date, category, desc, amount))
            amount = int(amount)
            total_expense_income += amount
            number += 1
        initialStr.set(f'The total above is {total_expense_income} dollars.')
    else:
        messagebox.showinfo("", "Category or date is not in the records")
    findEntry.delete(0, END)

def reset():
    for item in recordsTree.get_children():recordsTree.delete(item)
    number = 1
    total_expense_income = 0
    for date, category, desc, amount in records._records:
        recordsTree.insert('', 'end', text = str(number), values=(date, category, desc, amount))
        amount = int(amount)
        total_expense_income += amount
        number += 1
    balance = records._initial + total_expense_income
    initialStr.set("Now you have " + str(balance) + " dollars.")

def update():
    balance = 0
    try:
        initial = initialEntry.get()
        records._initial = int(initial)
    except:
        messagebox.showerror("Error", "Invalid value for money")
        initialEntry.delete(0, END)
    else:
        for i in records._records:
            balance += int(i[3])
        total = balance + int(initial)
        initialStr.set("Now you have " + str(total) + " dollars.")
        initialEntry.delete(0, END)

def categoryClick(event):
    global record
    category = categoryCombo.get().replace(' ', '', 13).replace('-','')
    record[1] = str(category)

def add_a_record():
    global record, number
    balance, total = 0,0
    _date = dateEntry.get_date().strftime("%Y-%m-%d")
    _desc = str(descEntry.get()) 
    _amount = str(amountEntry.get())
    if record[1] != '':
        if len(_desc.split()) == 1:
            if len(_amount.split()) == 1:
                try:
                    int(_amount)
                except:
                    messagebox.showerror("Error", "Invalid format of ammount")
                    amountEntry.delete(0, END)
                else:
                    record[0], record[2], record[3] = _date, _desc, _amount
                    records.add(record, categories)
                    recordsTree.insert('', 'end', text = str(number), values=(record[0], record[1], record[2], record[3]))
                    reset()
                    categoryCombo.delete(0, END)
                    descEntry.delete(0, END)
                    amountEntry.delete(0, END)
                    record = [0, '', 0, 0]
            else:
                messagebox.showerror("Error", "Invalid format fo ammount")
                amountEntry.delete(0, END)
        else:
            messagebox.showerror("Error", "Invalid format for description")
            descEntry.delete(0, END)
    else:
        messagebox.showerror("Error", "Please choose the category")
        categoryCombo.delete(0, END)
    

def delete():
    selected_item = recordsTree.selection()[0]
    selected_row = recordsTree.item(selected_item)
    line = selected_row['text']
    records.delete(line)
    reset()

#LEFT SIDE
#========================================================================================================================================#
findLabel = Label(root, text = "Find category or month ")
findEntry = Entry(root, width = 30, borderwidth = 3)
findButton = Button(root, padx = 4, text = "Find", command = lambda:find())
resetButton = Button(root, text = "Reset", command=reset)
findLabel.grid(row = 0, column = 0)
findEntry.grid(row = 0, column = 1)
findButton.grid(row = 0, column = 2)
resetButton.grid(row = 0, column = 3)

#Records Tree
#############################################################################################

#Create Treeview
recordsTree = ttk.Treeview(root)
recordsTree.grid(row = 1, column = 0,rowspan = 8, columnspan = 4)
recordsTree['columns'] = ("Date", "Category", "Description", "Amount")

#Create Scrollbar
vsb = ttk.Scrollbar(root, orient="vertical", command=recordsTree.yview)
vsb.place(x=390, y=27, height=223)
recordsTree.configure(yscrollcommand=vsb.set)

#Format or columns
recordsTree.column("#0", width=35, minwidth=35, anchor=W)
recordsTree.column("Date", anchor = W, width=70)
recordsTree.column("Category", anchor = W, width=115)
recordsTree.column("Description", anchor = W, width=115)
recordsTree.column("Amount", anchor = W, width=70)

#Create headings
recordsTree.heading("#0", text = "Line", anchor=CENTER)
recordsTree.heading("Date", text = "Date", anchor=W)
recordsTree.heading("Category", text = "Category", anchor=W)
recordsTree.heading("Description", text = "Description", anchor=W)
recordsTree.heading("Amount", text="Amount", anchor=W)

#Add data
number = 1
total_expense_income = 0
for datee, category, desc, amount in records._records:
    recordsTree.insert('', 'end', text = str(number), values=(datee, category, desc, amount))
    amount = int(amount)
    total_expense_income += amount
    number += 1
balance = records._initial + total_expense_income
#############################################################################################


initialStr = StringVar()
initialStr.set("Now you have " + str(balance) + " dollars.")
balance_label = Label(root, textvariable = initialStr)
deleteButton = Button(root, pady = 2, text = "Delete", command=delete)
balance_label.grid(row = 9, column = 0, columnspan=4, sticky=W)
deleteButton.grid(row = 9, column = 3, sticky = W)
#========================================================================================================================================#

#RIGHT SIDE
#========================================================================================================================================#
initialLabel = Label(root, text = "Initial money ")
initialEntry = Entry(root, width = 25, borderwidth=2)
initialLabel.grid(row = 1, column = 4, sticky = W)
initialEntry.grid(row = 1, column = 5)

updateButton = Button(root, pady = 4, text = "Update", command = update)
updateButton.grid(row = 2, column = 5, sticky = E)

dateLabel = Label(root, text = "Date")
dateEntry = DateEntry(root, width=22, selectmode = 'day', year = d.year, month = d.month, day = d.day)
dateLabel.grid(row = 4, column = 4, sticky=W)
dateEntry.grid(row = 4, column = 5)

categoryLabel = Label(root, text = "Category")
categoryLabel.grid(row = 5, column = 4, sticky=W)

categories_options = [
    '-expense', 
    '       -food', 
    '           -meal',
    '           -snack', 
    '           -drink', 
    '       -transportation', 
    '           -bus', 
    '           -railway', 
    '-income', 
    '       -salary', 
    '       -bonus'
]


categoryCombo = ttk.Combobox(root, width=22, value = categories_options)
categoryCombo.bind("<<ComboboxSelected>>", categoryClick)
categoryCombo.grid(row = 5, column = 5) 

descLabel = Label(root, text = "Description")
descEntry = Entry(root, width=25, borderwidth=2)
descLabel.grid(row = 6, column = 4, sticky=W)
descEntry.grid(row = 6, column = 5) 

amountLabel = Label(root, text = "Amount")
amountEntry = Entry(root, width = 25, borderwidth=2)
amountLabel.grid(row = 7, column = 4, sticky=W)
amountEntry.grid(row = 7, column = 5) 

addButton = Button(root, pady = 4, text = "Add a record", command = lambda:add_a_record())
addButton.grid(row = 8, column = 5, sticky=E)
#========================================================================================================================================#

root.mainloop()

records.save()