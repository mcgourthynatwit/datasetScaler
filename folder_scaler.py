"""
Scales and augments images within a directory by introducing various modifications with varying probabilities. 
    - 10% chance of horizontal flip.
    - 40% chance of Gaussian blurring.
    - 50% chance of edge enhancement.
    - Random brightness adjustments between -100 and 100.
    - Random rotation between -10 and 10 degrees.
    - Random shift in both X and Y directions.
    - Random noise addition.

Parameters:
- directory (str): The path to the root directory containing sub-folders with images.

Returns:
- None. For every image found in the directory, scaled and augmented versions are saved alongside the original with "_modified" appended to their names
"""

import os, cv2, random
import numpy as np
def folder_scaler(directory):
    if os.path.exists(directory): # directory exists
        scale = 5 # Scales folder by 5x, this number can change in future currently testing
        for folder in os.listdir(directory):
            folder_directory = os.path.join(directory, folder)
            for filename in os.listdir(folder_directory): # images in file
                file_directory = os.path.join(folder_directory, filename) # conjoins to make image directory
                if os.path.isfile(file_directory):
                    if any(file_directory.lower().endswith(extension) for extension in [".jpg", ".jpeg", ".png", ".bmp"]) and "_modified" not in filename.lower():
                        print("Processing file:", file_directory)

                        for _ in range(scale):
                            image = cv2.imread(file_directory)

                            # flip horizontal 10% chance
                            if(random.randint(1,10) >= 10):
                                image = cv2.flip(image,1)

                            # blur 40% chance
                            if random.randint(1,10) < 5:  
                                blur_value = random.randint(1, 5) * 2 + 1  # should be odd, greater than 1
                                image = cv2.GaussianBlur(image, (blur_value, blur_value), 0)

                            # edge enhancement 50% chance
                            if random.randint(1,10) > 5: 
                                kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=np.float32)
                                image = cv2.filter2D(image, -1, kernel)
                                
                            # brightness
                            brightness = random.uniform(-100,100)
                            image = cv2.add(image,brightness)

                            # rotation
                            angle = random.uniform(-10, 10) # rotate by a random angle between -30 and 30 degrees
                            M = cv2.getRotationMatrix2D((image.shape[1] / 2, image.shape[0] / 2), angle, 1)
                            image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

                            # shifting
                            shift = random.randint(-10, 10)
                            M = np.float32([[1, 0, shift], [0, 1, shift]]) # shift in both x and y direction
                            image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

                            # noise
                            noise = np.random.uniform(0,0.05, image.shape).astype('uint8')
                            image = cv2.add(image, noise)
                        
                            
                            # Save the modified image with a new filename
                            modified_file_directory = os.path.splitext(file_directory)[0] + "_modified" + str(_) + ".jpg"
                            cv2.imwrite(modified_file_directory, image)

                            print("Modified image saved at:", modified_file_directory)
                    else:
                        print("Skipping file:", file_directory, "- Not an image file")
    else:
        print("Directory not found.")