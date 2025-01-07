from nightgfx import process_image
# Example usage
input_image_path = input('Input image path of object\n(example: infra06, infra06.png)\n> ')  # Provide the input image path

process_image(input_image_path)

# Example automatic conversion
input_folder_path = input('Input folder name of images to convert\n> ')
from os import listdir, mkdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(input_folder_path) if isfile(join(input_folder_path, f)) and f[-4:].lower() == ".png"]
mkdir(f"{input_folder_path}/nightgfx")
for file in onlyfiles:
    process_image(f"{input_folder_path}/{file}", automatic_lights=True, output_image_path=f"{input_folder_path}/nightgfx/{file[:-4]}")