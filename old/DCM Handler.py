# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:46:26 2020

@author: harme
"""

import numpy as np
import matplotlib.pyplot as plt
import pydicom
from pydicom.data import get_testdata_files
import os

filename = "./LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/79262/1-068.dcm"
dataset = pydicom.dcmread(filename)


def load_data(filedir):
    ctarr = []
    metarr = []
    for filename in os.listdir(filedir):
        if filename.endswith(".dcm"):
            dataset = pydicom.dcmread(filedir+filename)
            ctarr.append(dataset.pixel_array)
            
            # print()
            # print("Filename.........:", filename)
            # print("Storage type.....:", dataset.SOPClassUID)
            # print()
            
            # pat_name = dataset.PatientName
            # display_name = pat_name.family_name + ", " + pat_name.given_name
            # print("Patient's name...:", display_name)
            # print("Patient id.......:", dataset.PatientID)
            # print("Modality.........:", dataset.Modality)
            # print("Study Date.......:", dataset.StudyDate)
            
            # if 'PixelData' in dataset:
            #     rows = int(dataset.Rows)
            #     cols = int(dataset.Columns)
            #     print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
            #         rows=rows, cols=cols, size=len(dataset.PixelData)))
            #     if 'PixelSpacing' in dataset:
            #         print("Pixel spacing....:", dataset.PixelSpacing)
            
            # # use .get() if not sure the item exists, and want a default value if missing
            # print("Slice location...:", dataset.get('SliceLocation', "(missing)"))
            
            metarr.append(float(dataset.SliceLocation))
            
    return ctarr, metarr


ctarr, metarr = load_data("./LCTSC/LCTSC-Test-S1-101/03-03-2004-08186/79262/")




# Normal mode:
print()
print("Filename.........:", filename)
print("Storage type.....:", dataset.SOPClassUID)
print()

pat_name = dataset.PatientName
display_name = pat_name.family_name + ", " + pat_name.given_name
print("Patient's name...:", display_name)
print("Patient id.......:", dataset.PatientID)
print("Modality.........:", dataset.Modality)
print("Study Date.......:", dataset.StudyDate)

if 'PixelData' in dataset:
    rows = int(dataset.Rows)
    cols = int(dataset.Columns)
    print("Image size.......: {rows:d} x {cols:d}, {size:d} bytes".format(
        rows=rows, cols=cols, size=len(dataset.PixelData)))
    if 'PixelSpacing' in dataset:
        print("Pixel spacing....:", dataset.PixelSpacing)

# use .get() if not sure the item exists, and want a default value if missing
print("Slice location...:", dataset.get('SliceLocation', "(missing)"))

# plot the image using matplotlib


print(np.array(dataset.pixel_array).shape)

#plt.imshow(dataset.pixel_array, cmap=plt.cm.bone)
#plt.show()


















