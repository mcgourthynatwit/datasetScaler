"""
Given a trained model, this function uses the Bing API to download images based on user prompts. 
Each image is then run through the model to evaluate its confidence against specified categories. 
If the model's confidence exceeds the set accuracy threshold, the image is saved to a specified directory. 
The function automates the retrieval and selection of images that align with the categories of interest, based on the confidence of a trained model.

Parameters:
- model_path: Path to the trained model.
- prompts: Dictionary linking folder names to search queries for the Bing API.
- directory: Destination directory where the curated images should be saved.
- model_directory: Temporary directory to store images downloaded from Bing before evaluating and curating.

Returns:
- None. Side effect is that images are saved in the specified directory if they meet the confidence threshold.

"""
from bing_image_downloader import downloader
import os, shutil
from fastai.vision.all import *

def predict_on_new_images(model_path, prompts, directory, model_directory):
    accuracy = 0.90 # threshold
    learn = load_learner(model_path)
    
    for folder, prompt in prompts.items(): 
        print('searching for images of ' , prompt)
        downloader.download(prompt, limit = 25, output_dir = model_directory, timeout = 5) # download using bing api , 25 images, 5s download limit
        downloaded_path = os.path.join(model_directory, prompt)
        for image_filename in os.listdir(downloaded_path):
            image_path = os.path.join(downloaded_path, image_filename) 
            print(image_path)
            pred, pred_idx, probs = learn.predict(image_path) 

            if probs[pred_idx] > accuracy: # If the prediction confidence is greater than the target accuracy, copy it to the destination folder
                destination_folder = Path(f'{directory}/{folder}')
                destination_folder.mkdir(parents=True, exist_ok=True)
                shutil.copy(image_path, destination_folder)
                print('File passed with confidence of ' , probs[pred_idx] , ' passed')
