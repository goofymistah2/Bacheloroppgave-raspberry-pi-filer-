# -*- coding: utf-8 -*-
"""
Created on Thu May  8 19:15:45 2025

@author: mrjay
""" 
import scipy as s
import random 
import numpy as np
import heapq
class Processing_handler: 
    def __init__(self):
        pass
    def shift_to_drop_start(self,threshold, list_of_lists, length,padding): 
        return_list_of_lists = []
        
        for e in list_of_lists: 
            for i in range(0,len(e)): 
               
                if (e[i]<=threshold): 
                    
                    return_list = [0 for j in range(0,length)]

                    for j in range(0,len(return_list)): 
                        index = i+j-padding
                        if ((index)>=0 and index<(len(e))):
                            return_list[j]=e[i+j-padding]
                        elif index>=len(e): 
                            corrective_sum = sum(e[-30:])/30
                            return_list[j]=corrective_sum
                        elif index<0: 
                            return_list[j]=e[0]
                
                    
                    return_list_of_lists.append(return_list)
                    
                    break 
        
        return return_list_of_lists
    
    
    def calculate_fft(self,list_of_lists,sampling_frequency=200):
        return_dict = {"f_axis": [],"yf1": [],"N": []}
        for e in list_of_lists:
            N = len(e)
            T = 1.0 / sampling_frequency
            yf1 = s.rfft(e)
            f_axis = s.rfftfreq(N, T)[:N//2]
            return_dict["N"].append(N)
            return_dict["yf1"].append(yf1)
            return_dict["f_axis"].append(f_axis)
        return return_dict
    def determine_cutoff(self,signals, cutoff_percentage=0.9): 
        fourier_transform = self.calculate_fft(signals)
        current_max = 0
        current_max_freq=0
        for i in range(0,len(fourier_transform["yf1"])): 
            signal = fourier_transform["yf1"][i]
            length = fourier_transform["N"][i]
            for j in range(0,length): 
                amplitude = np.abs(signal[j])/length
                if amplitude>current_max: 
                    current_max = amplitude
                    current_max_freq = fourier_transform["f_axis"][i][j]
        return cutoff_percentage*current_max_freq
    def lowpass(self,order,cutoff, signals, sampling_frequency=2000): 
        
        print(type(order), type(cutoff))
        cutoff = cutoff/(sampling_frequency/2)
        b,a = s.signal.butter(order,cutoff, "low")
        return_signals =[]
        for e in signals: 
            if (len(e)>18):
                print(type(e))
                return_signals.append(s.signal.filtfilt(b,a,e))
        return return_signals
    def correct_hall_sensor(self,hall_sensor_signals): 
        return_signals = []
        for e in hall_sensor_signals: 
            if (len(e)!=0): 
                corrective_sum = sum(e[-30:])/30
              
                for i in range(0,len(e)): 
                    
                    e[i]=e[i]-corrective_sum
                return_signals.append(e)
        return return_signals
   
    def get_peaks(self,list_of_lists): 
        filter_copy = list_of_lists.copy() 
        filter_copy = self.lowpass(5, 20, filter_copy)
        return_dict_list = {"peaks": [],"indices":[]}
        for i in range(0, len(filter_copy)): 
            current_peaks = []
            current_peaks_indices = s.signal.find_peaks(list_of_lists[i]) 
            indices = current_peaks_indices[0]
            return_dict_list["indices"].append(indices)
            for e in indices: 
                current_peaks.append(filter_copy[i][e])
            print(current_peaks)
            return_dict_list["peaks"].append(current_peaks)
        return return_dict_list
    def find_dampening_function(self,list_of_lists,sampling_rate=1000): 
        return_list = []
        peaks = self.get_peaks(list_of_lists)
        
        for i in range(len(peaks["peaks"])): 
            
            x = np.array(peaks["indices"][i],dtype=float)
            print(x)
            for j in range(0,len(x)): 
                x[j]=x[j]/sampling_rate
            print(x)
            current_peaks = peaks["peaks"][i]
            m,b = np.polyfit(x,np.log(current_peaks),1)
            return_list.append((m,b))
        return return_list
    def remove_defunct(self,list_of_lists,threshold):
        return_list = []
       
        peaks = []
        for i in range(0,len(list_of_lists)): 
            
            current_peaks_indices = s.signal.find_peaks(list_of_lists[i]) 
            
            current_peaks = []
            indices = current_peaks_indices[0]
            
            print(indices)
            previous_peak = list_of_lists[i][indices[0]]
            current_peaks.append(previous_peak)
            for e in indices: 
                current_peak = list_of_lists[i][e]
                
                if ((previous_peak-current_peak)>50):
                    print(current_peak)
                    current_peaks.append(current_peak)
                    previous_peak = current_peak
                    
            peaks.append(current_peaks[:5])
        
        median_peaks = np.median(peaks,axis=0)  
        
        
        for i in range(0, len(peaks)):
            cumulative_error = 0
            for j in range(0,len(peaks[i])): 
                print(peaks[i])
                print(median_peaks)
                cumulative_error+=peaks[i][j]/median_peaks[j]
        
            if (cumulative_error>threshold): 
                pass
            else: 
                return_list.append(list_of_lists[i])
        return return_list
        