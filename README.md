# Dataset Scaler

This project provides tools for scaling and augmenting image datasets, using the Bing image API. A pre-trained resnet34
model on the caltech 101 database is refined with user image folder to be trained to include the user category into the
model. The user prompts to search Bing for images and runs each image through the model and if images pass with an
valid confidence threshold they are then downloaded into the original user folder.

## Overview

- **Data Model Maker (`data_model_maker.py`)**: 
  - This script creates a data block model using the FastAI library. 
  - It loads a pre-trained recognition model(caltech 101 resnest 34), fine-tunes it, and then exports the model.
  
- **Main Script (`__main__.py`)**: 
  - This is the primary script that orchestrates the entire process. 
  - It validates the initial directory, prompts the user for model name, augments the data, calls function to refine model and then predicts on new images.
  
- **Copy Images (`copy_images.py`)**: 
  - This script copies a subset of images from the Caltech-101 dataset to a new directory.
  
- **Folder Scaler (`folder_scaler.py`)**: 
  - This script scales and augments images within a directory by introducing various modifications with varying probabilities, such as
    horizontal flip, Gaussian blurring, edge enhancement, brightness adjustments, rotation, shifting, and noise addition.
  
- **Predict Image (`predictImage.py`)**: 
  - This script loads a trained model and predicts on a new image, displaying the prediction, prediction index, and associated probabilities.
  
- **Train (`train.py`)**: 
  - This script sets up the data block and data loaders using the FastAI library, fine-tunes a model, and then saves the trained model.

## Usage

working on usage currently, may develop a front end ui 

## Dependencies

- FastAI
- OpenCV (cv2)
- NumPy
