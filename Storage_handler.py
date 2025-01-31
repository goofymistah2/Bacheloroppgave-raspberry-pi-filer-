#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 11:24:42 2025

@author: bachauto
"""

class Storage_handler: 
    def __init__(self): 
        self.storage_dict = {} 
    def append(self, key, array): 
        if (key in self.storage_dict): 
            self.storage_dict[key].extend(array)
        else: 
            self.storage_dict[key]=array
    def get_dict(self):
        return self.storage_dict
    def to_print(self): 
        for e in self.storage_dict: 
            print(self.storage_dict[e])
            