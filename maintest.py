# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 13:57:37 2025

@author: mrjay
"""

import library_handler as lib
import sqlite3


con = sqlite3.connect("tutorial.db")
cur=con.cursor() 
lib = lib.Library_handler(con,cur) 

lib.insert_drop_weight_data("0012",1,[1,2,3,4,5,6,7,8,9])
print(lib.get_test_results_drop_weight(1))
con.close()
