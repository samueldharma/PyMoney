# -*- coding: utf-8 -*-
"""
Created on Thu May 26 20:29:33 2022

@author: Samuel Sukatja
"""
from tkinter import *
import sys
from datetime import date as d
from tkinter import messagebox

class Record:
    """Represent a record."""
    def __init__(self, date, category, expense_income, amount):
        self._date = date
        self._category = category
        self._expense_income = expense_income
        self._amount = amount
    category = property(lambda self: self._category)
    desc = property(lambda self: self._expense_income)
    amount = property(lambda self: self._amount)

class Records:
    """Maintain a list of all the 'Record's and the initial amount of money."""
    balance = 0
    def __init__(self):
        self._records = []
        self._initial = 0
        try:
            with open('records.txt', 'r') as fh:
                if fh.read() == '':
                    pass
                else:
                    fh.seek(0)
                    try:
                        self._initial = int(fh.readline())
                        #reading files and make records 
                        self._records = [(i.replace('\n', '')).split(' ') for i in fh.readlines()]
                        for date, category, key1, value1 in self._records:
                            d.fromisoformat(date)
                            value1 = int(value1)
                    except ValueError:
                        messagebox.showerror('Error', 'Invalid format in records.txt\nDeleting the contents...')
                        with open('records.txt', 'w') as fh2:
                            fh2.writelines('') #deleting contents by overwriting the file
                            self._records = []
                    else:
                        print('Welcome back')
        except FileNotFoundError:
            messagebox.showwarning("Error", 'File not found')

    def add(self, record, categories):
        """Add record to records"""
        #record = record.split()
        try:
            #checking if there is 4 element in record
            if len(record) == 4:
                self._date, self._category, self._expense_income, self._amount = record
                self._record = Record(self._date, self._category, self._expense_income, self._amount)
            else:
                try:
                    self._category, self._expense_income, self._amount = record
                except ValueError:
                    raise ValueError
                self._date = str(d.today())
                record.insert(0, self._date)
                self._record = Record(self._date, self._category, self._expense_income, self._amount)
                
            try:
                d.fromisoformat(self._date)
                if categories.is_category_valid(self._category, categories._categories) == False:
                    print('The specified category is not in the category list.')
                    print('You can check the category list by command "view categories.')
                    print('Fail to add a record.')
                    self._record = []
                    return
                try:    
                    self._amount = int(self._amount)
                except ValueError:
                    print('Invalid value for money.')
                    print('Fail to add a record')
                else:
                    self._records.append(record)
            except ValueError:
                print('The format of date should be YYYY-MM-DD.')
                print('Fail to add a record.')
            
        except ValueError:
            print('The format of a record should be like this: breakfast 2020-06-08(optional) meal breakfast -50.')
            print('Fail to add a record.')
        
    
    def view(self):
        """To view records"""
        number = 1
        total_expense_income = 0
        print('No. Date       Category             Description          Amount')
        print('=== ========== ==================== ==================== ======')
        for date, category, keys, values in self._records:
            print(f'{str(number).center(3)} {date}  {category.ljust(20)} {keys.ljust(21)}{values.ljust(22)}')
            values = int(values)
            total_expense_income += values
            number += 1
        print('=== ========== ==================== ==================== ======') 
        balance = self._initial + total_expense_income
        print('Now you have %d dollars' %balance)

    def delete(self, delete):
        """Delete the desire record
        Parameter = numbers to delete seperate by comma and space (1, 2, 3, ...)
        """
        pops = 0
        subtractor = 0
        delete_split = delete.split(', ')
        
        for numdel in delete_split:
            try:
                numdel = int(numdel)
            except ValueError:
                print(f'Invalid format \'{numdel:s}\'. Fail to delete record')
            else:
                if int(numdel) <= 0: #check if input is negative numbers or zero
                    messagebox.showerror("Error", f'There is no record in record {numdel}. Fail to delete record.')
                else:
                    try:
                        pops = int(numdel) - 1 - subtractor #define index variable to pop
                        self._records.pop(pops)
                    except ValueError:
                        messagebox.showerror("Error", f'Invalid format \'{numdel}\'. Fail to delete record')
                    except IndexError:
                        messagebox.showerror("Error", f'There is no record in record {numdel}. Fail to delete record.')
                    else:
                        subtractor += 1
        subtractor = 0 #reset subtractor for next "delete" command
    def find(self, sub_cat):
        """Prompt for a category name to find"""
        number = 1
        total_expense_income = 0
        list_find = list(filter(lambda x : (x[1] in sub_cat) or (str(sub_cat) in x[0]), self._records))
        return list_find
        
    def save(self):
        """Saving when user input 'exit' """
        with open('records.txt', 'w') as fh:
            fh.write(str(self._initial))
            fh.write('\n')
            file = [' '.join(ele) for ele in self._records]
            for i in file:
                fh.write(i)
                fh.write('\n')

    def clear(self):
        """Clear all records"""
        with open('records.txt', 'w') as fh:
            fh.writelines('')
        self._records = []