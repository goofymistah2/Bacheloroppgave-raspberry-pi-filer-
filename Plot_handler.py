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
        self.data = []#må bevare en referanse til animasjonsvariabelen, ettersom FuncAnimation sendes som callback til update? 
    def append_data(self,new_data):
        self.data.extend(new_data)
    def fixed_interval_plot(self,start,stop): 
        x=[]
        y=[]
        for i in range(start,stop): 
            x.append(i) 
            y.append(self.data[i]) 
        plt.plot(x,y,'-') 
        plt.show()
            
    def get_len_of_data(self): 
        return len(self.data)
    def real_time_plot(self): 
        fig, ax = plt.subplots(figsize=(6,3))
        x = [0]
        y = [0]
        ln, = ax.plot(x, y, '-')
        def update(frame):
            x.append(x[-1] + 1)
            try: 
                y.append(self.data[0]) 
                self.data.pop(0)
            except: 
                print("no more data to be shown")
                return
            ln.set_data(x, y) 
            ax.relim() #dynamisk 
            ax.autoscale_view() 
            return ln,
        self.animation = FuncAnimation(fig, update, interval=500)
        plt.show()
    