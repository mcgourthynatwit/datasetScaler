from functions.validate_initial_directory import validate_initial_directory
import os
import multiprocessing as mp
from functions.predict_on_new_images import predict_on_new_images
from functions.make_model_folder import make_model_folder
from data_model_maker import modelMaker
if __name__ == '__main__':
    mp.set_start_method('spawn', force=True)
    directory = (r"C:\Users\mcgourthyn\Pictures\user_images")

    validate_initial_directory(directory)

    model_name = input('Name of model: ')

    print("Augmenting data...")
    model_directory = make_model_folder(directory, model_name) 
    
    model, model_directory = modelMaker(r"C:\Users\mcgourthyn\Pictures\user_images", model_directory)


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

    predict_on_new_images(model, prompts, directory, model_directory, 10) # 10 indicates that the model will search for and verify to download 10 images from bing
