#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 08:04:59 2025

@author: bachauto
"""
import sys
import json 
import paho.mqtt.client as paho
import threading 

class MQTT_handler():#en klasse som håndterer mqtt. Dette gjør det mye enklere å kombinere funksjonalitet i Main filen 
    

    def __init__(self): 
        self.client = paho.Client()
        self.client.username_pw_set("bachAuto","e2501")
        self.json_data_dictionary = {}
        if self.client.connect("localhost", 1883, 60) != 0:
            print("Couldn't connect to the mqtt broker")
            sys.exit(1)
        self.client.on_message = self.on_message
    def json_decode(self,json_string):
        try: 
            decoded_json_dict = json.loads(json_string) #decoder mottat streng og lagrer i en dictionary
            for e in decoded_json_dict.keys(): 
                self.json_data_dictionary[e] = decoded_json_dict[e] #lager en dictionary med de midlertidige verdiene, om flere en nyeste skal lagres håndteres ikke det i denne 
                
        except: 
            print("failed, received message possibly not in expected json format") 
        
            
        #skal implementeres
    def on_message(self,client,userdata,msg): 
        decoded = str(msg.payload.decode("utf-8"))
        self.json_decode(decoded)
        
        
    def _subscribe(self,topic): 
        self.client.subscribe(topic)
    def _publish(self,topic,payload): 
        self.client.publish(topic, payload)
    def poll(self,duration): 
        self.client.loop(duration)
    def _disconnect(self): 
        self.client.disconnect()
    def get_json_data_dictionary(self): 
        return self.json_data_dictionary