# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 14:34:47 2022

@author: Brian
"""

#load datasets

import csv
import os
import pandas
import matplotlib.pyplot as plt
import statistics

labels = ["As Received 10 mm/min (No Fracture)", "As Received 10 mm/min (No Fracture)", "As Received 100 mm/min", "2 Hr Air Cooled 100 mm/min",
          "As Received 100 mm/min", "2 Hr Air Cooled 100 mm/min","2 Hr Quenched 100 mm/min", "1 Hr Quenched", "1 Hr Air Cooled 100 mm/min", "1 Hr Air Cooled 100 mm/min",
          "As Received 100 mm/min","As Received 100 mm/min","As Received 100 mm/min","As Received 100 mm/min","Average As Received"]

cutoff = 6

datasets = list()

for filenum in range(1,15):
    datasets.append(open(f"C:\\Users\\Brian\\OneDrive - Massachusetts Institute of Technology\\2022-2023 School Year\\S1\\3.013\\Term Project\\datasets\\Specimen_RawData_{filenum}.csv").readlines())

def plot_combined_figure(indexes, data, stop = -1, xmin = 0, xlim = 550, ymin = 0, ylim = 130, plotmaximums = False):
    legend_labels = list()
    plt.figure(figsize=(9,6.5))
    plt.xlim([xmin,xlim])
    plt.ylim([ymin,ylim])
    plt.xlabel("Strain (%)")
    plt.ylabel("Engineering Stress (MPa)")
    total_ult = list()
    total_frac = list()
    for num, index in enumerate(indexes):
        us = round(ultimate[index],1)
        total_ult.append(us)
        frac = round(fracture[index],1)
        total_frac.append(frac)
        lab = labels[index]
        if plotmaximums: plt.plot([0,xlim],[us, us],':', label='_nolegend_')
        plt.scatter([x[0] for x in data[index][:stop]], [x[1] for x in data[index][:stop]])
        legend_labels.append(f"{lab} - σult {us}MPa - εfrac {frac}%")
    if len(indexes) > 1:
        plt.title("Average Ultimate Stress: " + str(round(sum(total_ult)/len(indexes),1))+ "MPa - Average Strain at Fracture: " + str(round(sum(total_frac)/len(indexes),1))+ "%\nUltimate Stress Deviation: " + str(round(statistics.stdev(total_ult),2))+ "MPa - Average Strain At Fracture Deviation: " + str(round(statistics.stdev(total_frac),2))+"%")
    else:
        plt.title("Average Ultimate Stress: " + str(round(sum(total_ult)/len(indexes),1))+ "MPa - Average Strain at Fracture: " + str(round(sum(total_frac)/len(indexes),1))+"%")
    plt.legend(legend_labels, loc="upper left")
    plt.show()
    
def plot_bulk_figure(indexes, data):
    for index in indexes:
        us = ultimate[index]
        plt.figure(figsize=(9,6.5))
        plt.xlim([0,550])
        plt.ylim([0,130])
        plt.title(labels[index])
        plt.xlabel("Strain (%)")
        plt.ylabel("Engineering Stress (MPa)")
        plt.scatter([x[0] for x in data[index]], [x[1] for x in data[index]])
        plt.show()

def average_lists(indexes, data):
    average = list()
    for i in range(max([len(x) for x in data])):
        tempsum = 0
        for dataset in indexes:
            try:
                tempsum += data[dataset][i][1]
            except:
                pass
        average.append(tempsum/len(indexes))
    return average

cleaned_datasets = list()
for dataset in datasets:
    cleaned_datasets.append([[float(y.replace('"',"")) for y in x.split(',')] for x in dataset[6:]])
    
reformatted_load_elongation = [[[y[1], y[2]] for y in x] for x in cleaned_datasets]

reformatted_stress_strain_intermediate1 = [[[(y[0]/96)*100, y[1]/2.405] for y in x] for x in reformatted_load_elongation]

#make all the data start at the same force.
reformatted_stress_strain_intermediate2 = list()
for dataset in reformatted_stress_strain_intermediate1:
    for index, datapoint in enumerate(dataset):
        if datapoint[1] > cutoff:
            reformatted_stress_strain_intermediate2.append(dataset[index:])
            break

reformatted_stress_strain = [[[y[0]-x[0][0], y[1]] for y in x] for x in reformatted_stress_strain_intermediate2]

ultimate = ([max([y[1] for y in x[:1000]]) for x in reformatted_stress_strain])
fracture = ([min([y[0] if y[1] < 10 else 1000 for y in x[150:]]) for x in reformatted_stress_strain])

print(fracture)

# plot_bulk_figure([0,1], reformatted_stress_strain)
    
# plot_combined_figure([2,10,11,12,13], reformatted_stress_strain)

# #2 Hr Air Cooled
# plot_combined_figure([3,5], reformatted_stress_strain)

# #1 Hr Air Cooled
# plot_combined_figure([9,8], reformatted_stress_strain)

# plot_combined_figure([7], reformatted_stress_strain)
# plot_combined_figure([6], reformatted_stress_strain)

# plot_combined_figure([2,10,11,12,13], reformatted_stress_strain, 300, 0, 60, 0, 120)

# plot_combined_figure([6,3,8,7,4], reformatted_stress_strain, 300, 0, 60, 60, 110, True)

# plot_combined_figure([3,5,6], reformatted_stress_strain)
# plot_combined_figure([7,8,9], reformatted_stress_strain)

plot_combined_figure(range(2,14), reformatted_stress_strain)






