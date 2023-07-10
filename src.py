import os
import cv2 
import random
import numpy as np
directory = input("Copy and paste folder directory with source images: ")

if os.path.exists(directory): # directory exists
    while True:
        scale = input("What is the scalar of this folder (e.g., 5: a folder with 10 images becomes 50 images): ")
        try:
            scale = int(scale)
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print("Valid scale entered:", scale)

    for filename in os.listdir(directory): # images in file
        placeholder = 0
        filepath = os.path.join(directory, filename) # conjoins to make image directory
        if os.path.isfile(filepath):
            if any(filepath.lower().endswith(extension) for extension in [".jpg", ".jpeg", ".png", ".bmp"]) and "_modified" not in filename.lower():
                print("Processing file:", filepath)

                for _ in range(scale):
                    image = cv2.imread(filepath)

                    # resize
                    scaleFactor = random.uniform(0.25, 2) 
                    image = cv2.resize(image, None, fx = scaleFactor, fy = scaleFactor)

                    #flip horizontal 10% of time
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
                        
                    # Salt-and-pepper noise
                    if random.randint(1,10) < 3:  # 30% chance to apply salt-and-pepper noise
                        row, col, _ = image.shape
                        salt_vs_pepper = 0.2
                        amount = 0.04
                        num_salt = np.ceil(amount * image.size * salt_vs_pepper)
                        num_pepper = np.ceil(amount * image.size * (1.0 - salt_vs_pepper))

                        # Add Salt noise
                        coords = [np.random.randint(0, i, int(num_salt)) for i in [row, col]]
                        image[coords[0], coords[1]] = 255

                        # Add Pepper noise
                        coords = [np.random.randint(0, i, int(num_pepper)) for i in [row, col]]
                        image[coords[0], coords[1]] = 0

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
                    modified_filepath = os.path.splitext(filepath)[0] + "_modified" + str(_) + ".jpg"
                    cv2.imwrite(modified_filepath, image)

                    print("Modified image saved at:", modified_filepath)
            else:
                print("Skipping file:", filepath, "- Not an image file")
else:
    print("Directory not found.")