import os
import shutil
from random import sample

OG_DIRECTORY = (r'C:\Users\mcgourthyn\Pictures\imageChunk') # partial piece of images used to train OG recongition model

DESTINATION_DIRECTORY = (r"C:\Users\mcgourthyn\Pictures\images")

for category_folder in os.listdir(OG_DIRECTORY):
    source_folder_path = os.path.join(OG_DIRECTORY, category_folder)
    
    # Ensure it's a folder
    if os.path.isdir(source_folder_path):
        images = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Randomly sample images
        sampled_images = sample(images, min(20, len(images)))

        dest_folder_path = os.path.join(DESTINATION_DIRECTORY, category_folder)
        if not os.path.exists(dest_folder_path):
            os.makedirs(dest_folder_path)

        # Copy each sampled image to destination folder
        for image_file in sampled_images:
            source_image_path = os.path.join(source_folder_path, image_file)
            dest_image_path = os.path.join(dest_folder_path, image_file)
            shutil.copy2(source_image_path, dest_image_path)
