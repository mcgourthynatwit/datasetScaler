"""
1. Verifies root directory of user images
2. Makes directory inside root directory with ending "_modelFolder"
3. Copies contents(user images) from root directory to modelFolder
4. Augments user images using folderScaler
5. Copies a portion of images used to train broad recognition model into modelFolder

Parameters:
- directory (str): The path to the root directory containing sub-folders (categories) with images.
- model_Name (str): The name of the model, which will be used to name the new model folder.

Returns:
- str: The path to the newly created model directory if successful.
- None: The function terminates the program if the validation conditions are not met.

"""
from folder_scaler import folder_scaler
from bing_image_downloader import downloader
import os, shutil
import folder_scaler as fs
from fastai.vision.all import *

def make_model_folder(directory, model_Name):
    if os.path.exists(directory): # 1
        model_folder = os.path.join(directory,  f"{model_Name}_modelFolder")  # 2
        for folder in os.listdir(directory): 
            destination_Folder = os.path.join(model_folder, str(folder)) 
            folder_path = os.path.join(directory, folder)  
            shutil.copytree(folder_path, destination_Folder) # 3
    else:
        return 
    
    folder_scaler(model_folder) # 4

    OG_DIRECTORY = (r"C:\Users\mcgourthyn\Pictures\images")
    for folder in os.listdir(OG_DIRECTORY): 
            destination_Folder = os.path.join(model_folder, str(folder)) 
            folder_path = os.path.join(OG_DIRECTORY, folder)  
            shutil.copytree(folder_path, destination_Folder) # 5

    print("Copy complete")
    return model_folder
