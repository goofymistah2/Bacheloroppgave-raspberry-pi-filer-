#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 08:41:38 2025

@author: bachauto
"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from random import randrange
import threading as t 
import sys
import json 
import paho.mqtt.client as paho
import threading 
import realtimeplot 
class Plot_handler():
   
    def __init__(self): 
        self.animation = None;
        self.data_dict = {}#må bevare en referanse til animasjonsvariabelen, ettersom FuncAnimation sendes som callback til update? 
    def append_data(self,new_data,key): #her legges data til ønsket liste (spesifisert med key)
        if (key in self.data_dict): #dette medfører et ganske tregt dictionary søk, kan endres senere for mer optimalisert kode
            self.data_dict[key].extend(new_data)
        else: 
            self.data_dict[key]=(new_data)
    def fixed_interval_plot(self,start,stop,key): #reading angir hvilken liste som skal plottes
        x=[]
        y=[]
        for i in range(start,stop): 
            x.append(i) 
            y.append(self.data_dict[key][i]) 
        plt.plot(x,y,'-') 
        plt.show()
            
    def get_len_of_data(self): 
        return len(self.data)
    def real_time_plot(self,key): 
        fig, ax = plt.subplots(figsize=(6,3))
        x = []
        y = []
        ln, = ax.plot(x, y, '-')
        def update(frame):
            x.append(x[-1] + 1)
            try: 
                y.append(self.data_dict[key][0]) 
            except: 
                print("no more data to be shown")
                return
            ln.set_data(x, y) 
            ax.relim() #dynamisk 
            ax.autoscale_view() 
            return ln,
        self.animation = FuncAnimation(fig, update, interval=500)
        plt.show()
    