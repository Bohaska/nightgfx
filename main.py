from PIL import Image
import numpy as np


# Function to desaturate a color
def desaturate_color(color):
    avg = int(np.mean(color))  # Calculate the average of the RGB values
    return avg, avg, avg  # Return the desaturated color


def process_image(input_image_path):
    # Open the input image
    if input_image_path[-4:] == ".png":
        img = Image.open(input_image_path)
    else:
        img = Image.open(input_image_path + ".png")
    bpp_img = img.convert('RGBA')
    img = img.convert("RGB")  # Convert image to RGB format

    transparent_colors = [
        (0, 0, 255),  # Blue
        (255, 255, 255)  # White
    ]

    # Define the target colors
    cc1_colors = [
        (8, 24, 88),  # #081858
        (12, 36, 104),  # #0c2468
        (20, 52, 124),  # #14347c
        (28, 68, 140),  # #1c448c
        (40, 92, 164),  # #285ca4
        (56, 120, 188),  # #3878bc
        (72, 152, 216),  # #4898d8
        (100, 172, 224)  # #64ace0
    ]

    cc1_mask_color = (40, 92, 164)

    preserve_colors = [
        (64, 0, 0),  # 239
        (255, 0, 0),  # 240
        (48, 48, 0),  # 241
        (64, 64, 0),  # 242
        (80, 80, 0),  # 243
        (255, 255, 0),  # 244
        (252, 60, 0),  # 232
        (252, 84, 0),  # 233
        (252, 104, 0),  # 234
        (252, 124, 0),  # 235
        (252, 148, 0),  # 236
        (252, 172, 0),  # 237
        (252, 196, 0),  # 238
    ]

    # Create an array of the image pixels
    img_data = np.array(img)

    # Create a blue background image
    blue_bg = np.array([0, 0, 255], dtype=np.uint8)
    result_img_data = np.full_like(img_data, blue_bg, dtype=np.uint8)

    for color in preserve_colors:
        mask = np.all(img_data == color, axis=-1)
        result_img_data[mask] = color  # Paste same color into mask

    # Create a mask for the cc1 colors
    mask = np.zeros(img_data.shape[:2], dtype=bool)

    for color in cc1_colors:
        mask = np.logical_or(mask, np.all(img_data == color, axis=-1))

    # Apply the mask and paste the selected area in the blue background
    result_img_data[mask] = cc1_mask_color  # Paste uniform color inside the selection

    # Convert the result back to an image
    result_img = Image.fromarray(result_img_data)

    mask_path = input_image_path + "--mask.png"
    # Save the resulting image
    result_img.save(mask_path)
    print(f"Processed mask saved to {mask_path}")

    bpp_img_data = np.array(bpp_img)
    for color in transparent_colors:
        mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)  # Find pixels that match the color
        bpp_img_data[mask] = (0, 0, 0, 0)  # Set them to fully transparent

    # Desaturate the cc1_colors
    for cc_color in cc1_colors:
        # Get a mask for pixels that match each color
        mask = np.all(bpp_img_data[:, :, :3] == cc_color, axis=-1)
        desaturated_color = desaturate_color(cc_color)  # Get the desaturated color
        bpp_img_data[mask, :3] = desaturated_color  # Apply desaturation to the RGB channels

    bpp_result_img = Image.fromarray(bpp_img_data)

    path = input_image_path + "--32bpp.png"
    bpp_result_img.save(path)
    print(f"Processed 32bpp saved to {path}")

# Example usage
input_image_path = input('Input image path of object\n(example: infra06, infra06.png)\n> ')  # Provide the input image path

process_image(input_image_path)
