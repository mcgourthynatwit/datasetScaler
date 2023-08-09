"""
Validates a specified directory for specific conditions to ensure it's suitable for model creation. The directory must
have atleast 1 sub-folder and each sub-folder must contain at least 10 images(.jpeg, .jpg, or .png).

Parameters:
- directory (str): The path to the root directory containing sub-folders (categories) with images.

Returns:
- None. If the directory doesn't meet the validation criteria, the function will print an error message and terminate the program.

Notes:
- The function checks for common image extensions such as .jpg, .jpeg, .png, and .bmp.
- Images with "_modified" in their filename are excluded from the count of original images.
- The function will terminate the program (`sys.exit()`) if the validation fails. This behavior can be changed if necessary.

Requires:
- os library to be imported. Ensure to also import 'sys' if the `sys.exit()` calls are to be retained.
"""

from bing_image_downloader import downloader
import os, sys, shutil, torch
import folder_scaler as fs
from fastai.vision.all import *

def validate_initial_directory(directory):
    categories = 0
    while True:
        #categories = int(input("How many categories of data do you have ? categories = #folders in root folder")) # update to handle error for string 
        #if(categories <= 1):
            #print('Must be more then 1 category to create model')
            #sys.exit()
        if os.path.exists(directory): # directory exists
                num_folders = 0
                for folder in os.listdir(directory): # folders
                    num_folders += 1
                    image_count = 0 
                    folder_path = os.path.join(directory, folder)

                    if os.path.isdir(folder_path):
                        for file_name in os.listdir(folder_path): # images in file
                            file_path = os.path.join(folder_path, file_name) # conjoins to make image directory
                            if os.path.isfile(file_path):
                                if any(file_path.lower().endswith(extension) for extension in [".jpg", ".jpeg", ".png"]):
                                    image_count += 1
                        if image_count <= 10 and not folder.lower().endswith('.pkl'):
                            print("folder named ", folder , "does not have 10 images, add some then run program again")
                            sys.exit() 
                if num_folders <= 1:
                    print("directory must have atleast 1 folders(1 or more categories for model)")
                    sys.exit() 
                else:
                    break
        else:
             print("Directory not found")
             sys.exit() 
