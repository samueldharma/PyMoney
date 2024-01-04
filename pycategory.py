# -*- coding: utf-8 -*-
"""
Created on Thu May 26 22:29:22 2022

@author: Samuel Sukatja
"""

class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        """Generate categories"""
        self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

    def view(self, L, level = 0):
        """This is view categories function
        Indent using recursive 
        """
        if type(L) == list:
            for child in L:
                self.view(child, level+2)
        else:
            print(f'{" " * 1 * level}- {L}')
        
    def is_category_valid(self, category, categories):
        """Checking if the input category is in categories
        Returns True if category is in categories and False otherwise
        """
        if type(categories) != list:
            if category == categories:
                return True
        else:
            for child in categories:
                a = self.is_category_valid(category, child)
                if a == True:
                    return True
            return False
    
    def find_subcategories(self, category, categories):
        """To find sub categories"""
        def find_subcategories_gen(category, categories, found=False):
            if type(categories) == list:
                for index, child in enumerate(categories):
                    yield from find_subcategories_gen(category, child, found)
                    if child == category and index + 1 < len(categories) \
                        and type(categories[index + 1]) == list:
                        # When the target category is found,
                        # recursively call this generator on the subcategories
                        # with the flag set as True.
                        yield from find_subcategories_gen(categories, categories[index+1], True)
            else:
                if categories == category or found == True:
                    yield categories
        return list(find_subcategories_gen(category, categories))