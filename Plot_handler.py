#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 08:41:38 2025

@author: bachauto

"""
import matplotlib 

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
   
    def __init__(self,storage_dict): 
        self.animation = None#må bevare en referanse til animasjonsvariabelen, ettersom FuncAnimation sendes som callback til update? 
        self.storage_dict = storage_dict 
    def fixed_interval_plot(self,key,start,stop): #reading angir hvilken liste som skal plottes
        x=[]
        y=[]
        array = self.storage_dict.get_dict()[key]
        for i in range(start,stop): 
            x.append(i) 
            y.append(array[i])
        plt.plot(x,y,'-') 
        plt.show()
            
    def get_len_of_data(self): 
        return len(self.data)
    def real_time_plot(self,key): 
        fig, ax = plt.subplots(figsize=(6,3))
        x = []
        y = []
        ln, = ax.plot(x, y, '-')
        i=0
        def update(frame):
            global i
            x.append(i)
            array = self.storage_dict.get_dict()[key]
            
            y.append(array[i])
            
            ln.set_data(x, y) 
            ax.relim() #dynamisk 
            ax.autoscale_view() 
            i+=1
            return ln,
        self.animation = FuncAnimation(fig, update, interval=500)
        plt.show()
    