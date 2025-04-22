# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17 13:22:26 2025

@author: mrjay
"""
import sqlite3


class Library_handler(): 
    def __init__(self, con, cur): 
       self.con = con
       self.cur = cur
       
       self.setup()
    def setup(self): 
        
        self.cur.execute("CREATE TABLE IF NOT EXISTS oring(ring_id TEXT PRIMARY KEY, colour TEXT, dimension INTEGER, batch INTEGER, number INTEGER)")
        self.cur.execute("CREATE TABLE IF NOT EXISTS dropweighttest(ring_id TEXT, testNumber INTEGER, arrayIndex INTEGER, value INTEGER,PRIMARY KEY (ring_id, testNumber, arrayIndex), FOREIGN KEY (ring_id) references oring(ring_id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS pendulumtest(ring_id TEXT, testNumber INTEGER, arrayIndex INTEGER, value INTEGER ,PRIMARY KEY (ring_id, testNumber, arrayIndex),FOREIGN KEY (ring_id) references oring(ring_id))")
        self.cur.execute("CREATE TABLE IF NOT EXISTS vibrationtest(ring_id TEXT, testNumber INTEGER, arrayIndex INTEGER, value INTEGER,PRIMARY KEY (ring_id, testNumber, arrayIndex), FOREIGN KEY (ring_id) references oring(ring_id))")
        
    def cleanup(self):
        self.cur.execute("DROP TABLE IF EXISTS oring")
        self.cur.execute("DROP TABLE IF EXISTS dropweighttest")
        self.cur.execute("DROP TABLE IF EXISTS pendulumtest")
        self.cur.execute("DROP TABLE IF EXISTS vibrationtest")
    def insert_drop_weight_data(self,ring_id, testNumber,values):
        index_range = range(0,len(values)) 
        insert_data = [(ring_id, testNumber,i,values[i]) for i in index_range]
        self.cur.executemany("INSERT OR IGNORE INTO dropweighttest(ring_id,testNumber,arrayIndex,value) VALUES (?,?,?,?)",insert_data)
        self.con.commit()
    def get_test_results_drop_weight(self,testNumber): 
        self.cur.execute("SELECT value FROM dropweighttest WHERE testNumber = ? ORDER BY arrayIndex ASC", (testNumber,))
        self.con.commit()
        return_list = [row[0] for row in self.cur]
        return return_list
    def get_test_results_pendulum(self,testNumber): 
        self.cur.execute("SELECT value FROM pendulumtest WHERE testNumber = ? ORDER BY arrayIndex ASC", (testNumber,))
        self.con.commit()
        return_list = [row[0] for row in self.cur]
        return return_list
    def get_test_results_vibration(self,testNumber): 
        self.cur.execute("SELECT value FROM vibrationtest WHERE testNumber = ? ORDER BY arrayIndex ASC", (testNumber,))
        self.con.commit()
        return_list = [row[0] for row in self.cur]
        return return_list
    
        
    def insert_pendulum_data(self,ring_id, testNumber,values):
        index_range = range(0,len(values)) 
        insert_data = [(ring_id, testNumber,i,values[i]) for i in index_range]
        self.cur.executemany("INSERT OR IGNORE INTO pendulumtest(ring_id,testNumber,arrayIndex,value) VALUES (?,?,?,?,?)",insert_data)
        self.con.commit()
    def insert_vibration_data(self,ring_id, testNumber,values):
        index_range = range(0,len(values)) 
        insert_data = [(ring_id, testNumber,i,values[i]) for i in index_range]
        self.cur.executemany("INSERT OR IGNORE INTO vibrationtest(ring_id,testNumber,arrayIndex,value) VALUES (?,?,?,?,?)",insert_data)
        self.con.commit()
    