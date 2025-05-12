# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:15:45 2025

@author: mrjay
"""
from scipy.fft import rfft,rfftfreq
import random 
import math 

class processing_handler: 
    def __init__(self):
        pass
    def shift_to_drop_start(threshold, list_of_lists): 
        return_list_of_lists = []
        
        for e in list_of_lists: 
            for i in range(1,len(e)): 
                if (e[i]<=threshold): 
                    return_list_of_lists.append(e[i:len(e)])
                    break 
        return return_list_of_lists
    
    
    def calculate_fft(self,accel1,sample_rate=200):
       
        
 
        N = len(accel1)
        T = 1.0 / sample_rate
        yf1 = rfft(accel1)
        f_axis = rfftfreq(N, T)[:N//2]
        
        return {
            "f_axis": f_axis,
            "yf1": yf1,
           
            "N": N
        }


