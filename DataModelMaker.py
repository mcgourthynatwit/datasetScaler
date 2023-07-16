# Creates a datamodel for image classification that will search bing images to add to dataset. Requires 10 images and uses the folderScalar 
# function to scale those 10 to a higher dataset size. The results found in bing are ran through the model and expect 90% accuracy to save to 
# data folder. Reason goes a long with the folder scalar scaling image datasets but furthermore I experienced issues with fast.ai search_ddg
# producing incorrect images ie. 10 dollar bill search saving 1 dollar bills, black labs saving more general lab breeds. 

# current errors
# 1. learn.predict is not running will fix today
# 2. categories input is commented out for testing speed purposes
# 3. overall error handling, and need to format code a bit better
# 4. general ux (prompting user with target accuracy)
# 5. optimization of model, batch size, epochs, currently valid_loss is getting extremely low so model may be memorizing -- may need more data 

from bing_image_downloader import downloader
import os, sys, shutil, torch
import FolderScaler as fs
from fastai.vision.all import *


def makeModelFolderDirectory(directory, model_Name):
    if os.path.exists(directory):
        model_folder = os.path.join(directory,  f"{model_Name}_modelFolder")
        for folder in os.listdir(directory):
            destination_Folder = os.path.join(model_folder, str(folder)) 
            folder_path = os.path.join(directory, folder)  
            shutil.copytree(folder_path, destination_Folder)
        print("Copy complete")
        return model_folder

def validateInitialDirectory(directory):
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
                    imageNumbers = 0 # check if folder has at least 10 jpegs
                    folder_path = os.path.join(directory, folder)

                    if os.path.isdir(folder_path):
                        for filename in os.listdir(folder_path): # images in file
                            filepath = os.path.join(folder_path, filename) # conjoins to make image directory
                            if os.path.isfile(filepath):
                                if any(filepath.lower().endswith(extension) for extension in [".jpg", ".jpeg", ".png", ".bmp"]) and "_modified" not in filename.lower():
                                    imageNumbers += 1
                        if imageNumbers <= 10:
                            print("folder named ", folder , "does not have 10 images, add some then run program again")
                            sys.exit()
                if num_folders <= 1:
                    print("directory must have atleast 2 folders(2 or more categories for model)")
                    sys.exit()
                else:
                    break
        else:
             print("Directory not found")
             sys.exit()

def predict_on_new_images(model_path, prompts, directory, model_directory):
    accuracy = 0.995 # want 97% accuracy for downloaded images
    learn = load_learner(model_path)
    
    for folder, prompt in prompts.items(): 
        # create temporary folder inside model_directory
        print('searching for images...')
        downloader.download(prompt, limit = 25, output_dir = model_directory, timeout=60)
        downloaded_path = os.path.join(model_directory, prompt)
        for image_filename in os.listdir(downloaded_path):
            image_path = os.path.join(downloaded_path, image_filename)  # get the full image path
            print(image_path)
            pred, pred_idx, probs = learn.predict(image_path) # this line needs fix

            # If the prediction confidence is greater than the target accuracy, copy it to the destination folder
            if probs[pred_idx] > accuracy:
                destination_folder = Path(f'{directory}/{folder}')
                destination_folder.mkdir(parents=True, exist_ok=True)
                shutil.copy(image_path, destination_folder)

def modelMaker(directory):   
        validateInitialDirectory(directory)
        #modelName = input('Name of model: ')

        model_directory = makeModelFolderDirectory(directory, "modelName") # this line will be changed after testing
        fs.folderScaler(model_directory)
        print("model folder scaled")

        print("Loading images into model")
        fns = get_image_files(model_directory)
        print(fns)

        # Create a DataBlock and DataLoaders
        print("Creating datablock model")
        data_block = DataBlock(
            blocks=(ImageBlock, CategoryBlock),
            get_items=get_image_files,
            splitter=RandomSplitter(valid_pct=0.65, seed=30),
            get_y=parent_label,
            item_tfms=Resize(128, method = 'pad')
        )
        print("Loading data into datablock")
        dataLoad = data_block.new(item_tfms=RandomResizedCrop(224, min_scale=0.5),batch_tfms=aug_transforms())
        dls = dataLoad.dataloaders(directory, bs = 100, num_workers = 0)
        dls.one_batch()
        print("Testing model")
        learn = vision_learner(dls, resnet34, metrics=error_rate)

        print("Find tuning model")
        learn.fine_tune(1, base_lr=3e-3, freeze_epochs=6, cbs=EarlyStoppingCallback(monitor='valid_loss', min_delta=0.01, patience=3))

        # Save the trained model
        model = os.path.join(model_directory, "model.pkl")
        learn.export(model)        
        print("Model created and saved")

        prompts = {}
        for folder in os.listdir(directory):
            if folder.endswith(('_modelFolder' , '.pkl')):
                continue  # do nothing
            else:
                while True:
                    user_enter = input(f"what prompt do you want searched for images in folder {folder}")
                    confirmation = input(f"confirm prompt {user_enter} (y/n)")
                    if confirmation.upper() == 'Y':
                        prompts[folder] = user_enter
                        break
                       
             
             
        predict_on_new_images(model, prompts, directory, model_directory)
    
 

    
