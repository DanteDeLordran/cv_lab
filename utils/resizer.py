import os
from PIL import Image
from tkinter import filedialog

def resize_and_crop(image_path, output_path, new_width, new_height):
    try:
        # Open the image
        img = Image.open(image_path)
        original_width, original_height = img.size

        # Resize the image while maintaining the aspect ratio to cover the new size
        img_ratio = original_width / original_height
        new_ratio = new_width / new_height

        if img_ratio > new_ratio:
            # If the image is wider, adjust the height
            img = img.resize((int(new_height * img_ratio), new_height), Image.LANCZOS)
        else:
            # If the image is taller, adjust the width
            img = img.resize((new_width, int(new_width / img_ratio)), Image.LANCZOS)

        # Crop the image to the center to match the new dimensions
        left = (img.width - new_width) // 2
        top = (img.height - new_height) // 2
        right = left + new_width
        bottom = top + new_height

        img = img.crop((left, top, right, bottom))

        # Save the final image
        img.save(output_path)
        print(f"Image saved: {output_path}")
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")

def process_images_in_directory(directory_path, new_width, new_height, output_directory=None):
    if not os.path.isdir(directory_path):
        print(f"Directory does not exist: {directory_path}")
        return

    if output_directory:
        os.makedirs(output_directory, exist_ok=True)
    else:
        output_directory = directory_path

    # Process each file in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(directory_path, filename)
            output_path = os.path.join(output_directory, filename)
            resize_and_crop(input_path, output_path, new_width, new_height)
        else:
            print(f"Skipping non-image file: {filename}")

# Usage
input_folder = filedialog.askdirectory()
output_folder = filedialog.askdirectory()
width = 700
height = 525

process_images_in_directory(input_folder, width, height, output_folder)
