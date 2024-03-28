# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 08:58:35 2024

@author: Administrator
"""

import numpy as np
from shapely.geometry import Polygon, Point
import pickle
import pandas as pd
from stardist import random_label_cmap, _draw_polygons, export_imagej_rois

def count_stardist_labels_inside_polygon(stardist_labels, polygon_points,details_stardist):
    polygon = Polygon(polygon_points)
    count = 0
    index_label = 0
    index_all = []
    for label in np.unique(stardist_labels):
        # Assuming stardist_labels is an array with the same shape as the image
        # Check if label centroid is inside the polygon
        if label != 0:  # 0 usually represents background
            label_indices = np.where(stardist_labels == label)
            label_centroid = np.mean(label_indices, axis=1)
            if polygon.contains(Point(label_centroid[1], label_centroid[0])):  # shapely Point takes (x, y)
                count += 1
                print(count)
                index_all.append(index_label)
        index_label = index_label + 1
    new_details = details_stardist['coord']
    new_details1 = new_details[index_all]
    # #%Export rois to imagej
    export_imagej_rois("X:\\Users\\Members\\Yael_Kashash\\All Images\\cfos exp\\Social group\\BMR20\\tifs for OT count\\testnew.zip", new_details1) 
    return count

# Function to read coordinates from CSV
def read_coordinates_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    coordinates = df[['X', 'Y']].values.tolist()
    labels = df['Label'].values.tolist()
    return coordinates, labels


# Example usage:
    
    
    
# Example usage
detailsp =  "X:\\Users\\Members\\Yael_Kashash\\All Images\\cfos exp\\Social group\\BMR20\\tifs for OT count\\details.pkl"
labelsp ="X:\\Users\\Members\\Yael_Kashash\\All Images\\cfos exp\\Social group\\BMR20\\tifs for OT count\\labels.npy"
image_path = 'X:\\Users\\Members\\Yael_Kashash\\All Images\\cfos exp\\Social group\\BMR20\\tifs for OT count\\Oxytocin\\127_BMR20_Slide18_6.tif'
csv_file = 'X:\\Users\\Members\\Yael_Kashash\\All Images\\cfos exp\\Social group\\BMR20\\tifs for OT count\\Coord.csv'
coordinates,labels = read_coordinates_from_csv(csv_file)


# Load the labels array using numpy
#labels_stardist = np.load(labelsp,allow_pickle=False)

## Open the pickle file and load the dictionary

with open(detailsp, 'rb') as fp:
    
     details_stardist = pickle.load(fp)
     
stardist_labels = np.load(labelsp)

    
    
    
    
condition = lambda x:  x == 0  # Check if the element is even

# Use list comprehension to get indices of elements that satisfy the condition
indices = [index for index, element in enumerate(labels) if condition(element)]
selected_data = [coordinates[index] for index in indices]
polygon_points = [(x, y) for x, y in selected_data]

#polygon_points = [(1, 1), (1, 3), (3, 3), (3, 1)]  # Example polygon points

count = count_stardist_labels_inside_polygon(stardist_labels, polygon_points,details_stardist)
print("Number of stardist labels inside the polygon:", count)