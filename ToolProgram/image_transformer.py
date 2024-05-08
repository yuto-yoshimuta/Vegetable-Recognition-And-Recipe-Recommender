# import necessary modules from the python imaging library (pil)
from pil import image, imageenhance, imageops
# import the os module for working with the operating system
import os

# define a function to transform an image with specified parameters
def transform_image(input_path, output_path, rotation_angle=0, flip_horizontal=False, brightness_factor=1.0):
    # open the original image using pil
    original_image = image.open(input_path)
    # rotate the image by the specified angle
    rotated_image = original_image.rotate(rotation_angle)

    # check if horizontal flipping is requested and perform the operation
    if flip_horizontal:
        rotated_image = imageops.mirror(rotated_image)

    # create an imageenhance object for adjusting brightness
    enhancer = imageenhance.brightness(rotated_image)
    # adjust the brightness of the image using the specified factor
    brightened_image = enhancer.enhance(brightness_factor)

    # save the transformed image to the specified output path
    brightened_image.save(output_path)
    # print a message indicating the completion of the transformation
    print(f"Transformation completed: {input_path} → {output_path}")

# define a function to batch transform images in a directory
def batch_transform_images(input_dir, output_dir, rotation_angle=0, flip_horizontal=False, brightness_factor=1.0):
    # check if the output directory exists; if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # loop through all files in the input directory
    for filename in os.listdir(input_dir):
        # check if the file has a valid image file extension
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # construct the full input and output paths for the current image
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            # call the transform_image function with specified parameters
            transform_image(input_path, output_path, rotation_angle, flip_horizontal, brightness_factor)

# entry point of the script; executed if the script is run as the main program
if __name__ == "__main__":
    # define input and output directories
    input_directory = "input_images"
    output_directory = "transformed_images"

    # set transformation parameters
    rotation_angle = 90
    flip_horizontal = True
    brightness_factor = 1.2

    # call the batch_transform_images function with specified parameters
    batch_transform_images(input_directory, output_directory, rotation_angle, flip_horizontal, brightness_factor)

    # print a message indicating the completion of all image transformations
    print("All image transformations completed.")
