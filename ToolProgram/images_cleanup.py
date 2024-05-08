from PIL import Image
import os
from hashlib import md5

# function to calculate the md5 hash of the image data
def calculate_hash(image_path):
    try:
        with Image.open(image_path) as image:
            return md5(image.tobytes()).hexdigest()
    except Exception as e:
        print(f"an error occurred: {e}")
        return None

# function to resize the image to a specified target size
def resize_image(image_path, target_size=(221, 221)):
    with Image.open(image_path) as image:
        resized_image = image.resize(target_size).convert("RGB")
        return resized_image

# function to rename files and remove duplicates based on hash values
def rename_and_remove_duplicates(folder_path, target_size=(221, 221)):
    hash_dict = {}

    # iterate through the files in the specified folder
    for i, filename in enumerate(os.listdir(folder_path)):
        # check if the file has a valid image file extension
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(folder_path, filename)
            
            # calculate the hash value for the image
            hash_value = calculate_hash(file_path)

            # skip the file if an error occurs during hash calculation
            if hash_value is None:
                print(f"skipped file due to an error: {filename}")
                continue

            # check for duplicate images and remove them
            if hash_value in hash_dict:
                print(f"detected duplicate image: {filename}")
                print(f"removed {filename}.")
                os.remove(file_path)
            else:
                # update the hash dictionary with the current hash value and file path
                hash_dict[hash_value] = file_path

                # rename the file to a standardized format
                new_name = f'image_{i + 1:03d}{os.path.splitext(filename)[1]}'
                new_path = os.path.join(folder_path, new_name)

                # rename the file and print the information
                os.rename(file_path, new_path)
                print(f'renamed: {filename} → {new_name}')

                # resize the image and save it with the new name
                resized_image = resize_image(new_path, target_size)
                resized_image.save(new_path)

if __name__ == "__main__":
    # specify the folder path containing the images
    folder_path = "path"
    # specify the target size for resizing the images
    target_size = (221, 221)
    # execute the main function to rename and remove duplicates
    rename_and_remove_duplicates(folder_path, target_size)
    # print a message indicating that the process is finished
    print("finished")