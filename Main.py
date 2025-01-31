#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:00:54 2025

@author: bachauto
"""
import MQTT_handler as M
import Plot_handler as P 
import matplotlib 

import matplotlib.pyplot as plt

import threading as thr
import Storage_handler as st
from matplotlib.animation import FuncAnimation


plt.close('all')
storage_handler = st.Storage_handler() #storage handler er en klasse. Det lages en instans som aksesseres av både plot_handler og mqtt_handler. 
#Mqtt_handler legger inn data og plot_handler henter ut
mqtt_handler = M.MQTT_handler(storage_handler) 
plot_handler = P.Plot_handler(storage_handler) 

mqtt_handler._publish("sensor1", "koblet til")
mqtt_handler._subscribe("sensor1")

callable_dictionary = {"rt": plot_handler.real_time_plot, "fint": plot_handler.fixed_interval_plot}

#for i in range(0,100): 
    #mqtt_handler.poll(0.1); 
    #try: 
       #plot_handler.append_data(mqtt_handler.get_json_data_dictionary()["readings"],"readings")
    #except:
      #print("no data to fetch")

mqtt_thread = thr.Thread(target=mqtt_handler.continuous_poll, daemon=True) #henting av data skjer i bakgrunnen i en separat tråd. Gjør at den kan samhandle med resten av programmet 
mqtt_thread.start()

while(True): #big while loop hvor mesteparten av systemfunksjonaliteten skjer 
    command = input("...")
    
    command = command.split(" ") #bryter ned inputstreng i biter som brukes til å kalle på relevant funksjon med tilhørende parametere
    if (command[0]=="rt"): 
        print(type(command[1]))
        plot_handler.real_time_plot(command[1]) 
    elif (command[0]=="fint"): 
        plot_handler.fixed_interval_plot(command[1], int(command[2]), int(command[3])) 
    elif (command[0]=="x"): 
        break 
        
    

mqtt_handler._disconnect()
mqtt_thread.join()  


