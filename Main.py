#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 12:00:54 2025

@author: bachauto
"""
import MQTT_handler as M
import Plot_handler as P 
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation

plt.close('all')
mqtt_handler = M.MQTT_handler() 
plot_handler = P.Plot_handler() 
mqtt_handler._publish("testTopic2", "klasseimplementasjon funker")
mqtt_handler._subscribe("testTopic2")
for i in range(0,100): 
    mqtt_handler.poll(0.1); 
    try: 
        plot_handler.append_data(mqtt_handler.get_json_data_dictionary()["readings"],"readings")
    except:
        print("no data to fetch")
plot_handler.fixed_interval_plot(0, 10,"readings")
mqtt_handler._disconnect()
 


