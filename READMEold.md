# Generate_Labels.py

This function serves to preprocess our the data provided by the AAMP competition.
Dicom segmentation files are taken and converted to 3D binary masks, one per organ, and saved as .npy files. 
CT dicoms are preprocessed and saved volumetrically as .npy files.

## Getting started

### Download data
Data can be downloaded from: https://wiki.cancerimagingarchive.net/display/Public/Lung+CT+Segmentation+Challenge+2017
Data is stored in following file structure:
	NBIA_CT_Data > LCTSC > [Sample Folders] > A Single Folder > [Dicom folder, segmentation folder] > Dicom files
The program processes the data assuming you have this file structure. It will not run correctly otherwise. 

### Prerequisites
The following modules are required:
Matplotlib
Pydicom
glob
numpy
skimage


## Running program

### Variables
plot_figs: controls whether the program displays example slices for each CT volume and segemntation
d: directory location of LCTSC 
d_out_data, d_out_label: Output directories for generated labels and CT volumes



# 3d_2d_conversion.ipynb

This function takes the 3d .npy files made by Generate_Labels.py and generates 512x512 2D slices. 
They are saved as individual .npy files. It first does this for the CT volumes, then for the individual
organ segmentations. Organ slices are saved to an organ specific folder.

## Prerequisites
the following modules are required:
numpy

## Running the program

### Variables:
data_dir, seg_dir: Output directories of Generate_Labels.py
save_data_dir, save_heart_dir, save_eso_dir, save_lungR_dir, save_lungL_dir, save_spine_dir: Directory to save
2D slices. Folders should be created prior to running program.



# 2D_UNet_Final.ipynb

This is the main script that loads CT slices, preprocesses data, runs, and fits the model. The code starts with the full
2D Unet architecture, then preprocesses data used from 3D_2D_conversion, and finally predicts and saved the predictions. 


## Prerequisites
the following modules are required:
numpy
tensorflow
sklearn
matplotlib

## Running the program

### Variables:
label, seg_dir: input directories and namespaces of the organ that will be used for the rest of the code
cut_train_files, empty_train_files: Arrays that split training images into sparse and not sparse masks (used as part of dealing with class imbalance of heart)
comb_train_files, comb_val_files, comb_test_files: Arrays that hold equal combinations of sparse and non-sparse CT scan segmentations
train_gen, val_gen: generator functions that generate training and validation data for model
history: tensorflow objects that holds all the value over epoch information
savename_pred, savename_mask: directories to  which the predictions will be saved


## 2D Unet

Defines Unet architecture to be used in the training model section. 
x_2d.summary gives a input/output summary that shows dimensionatlity. 
This could be useful in the case that input dimensions dont match in the training section. 


## Train Model

Loads in data using train_gen and val_gen using the generators from the preprocessing section. 
batch_size determines how many CT stacks can be injested with each call to the generator function. 
dice_loss and mean_iou define functions that are used as metrics in the fit model.
x_2d.fit officially runs te model, with input parameters as defined before. 
A callback function is used for checkpoints. Make sure to change checkpoint_path in accordance with your directory.
history object stores values over epoch and allows for plotting in the next cell.


## Load Weights, Visualize, Save Predictions

x_2d.load_weights loads existing weights with directory as input, only applicable if model was ran previously.
savename_pred and savename_mask save prediction and slice masks according to the directory and file name inputed. 
data and mask objects should change according to the naming covention of your CT files. 

