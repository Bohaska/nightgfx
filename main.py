from PIL import Image
import numpy as np


# Function to desaturate a color
def desaturate_color(color):
    avg = int(np.mean(color))  # Calculate the average of the RGB values
    return avg, avg, avg  # Return the desaturated color


def process_image(input_image_path):
    # Open the input image
    if input_image_path[-4:] == ".png":
        input_image_path = input_image_path[:-4]
    img = Image.open(input_image_path + ".png")

    PALETTE = img.getpalette()

    transparent_colors = [
        (0, 0, 255),  # Blue
        (255, 255, 255)  # White
    ]

    # Define the target colors
    cc1_palette_colors = [198, 199, 200, 201, 202, 203, 204, 205]

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

    cc1_mask_color = 202

    cc2_palette_colors = [80, 81, 82, 83, 84, 85, 86, 87]

    cc2_colors = [
        (8, 52, 0),
        (16, 64, 0),
        (32, 80, 4),
        (48, 96, 4),
        (64, 112, 12),
        (84, 132, 20),
        (104, 148, 28),
        (128, 168, 44),
    ]

    cc2_mask_color = 84

    preserve_palette_colors = [239, 240, 241, 242, 243, 244, 232, 233, 234, 235, 236, 237, 238]

    # Create an array of the image pixels
    img_data = np.array(img)

    # Create a blue background image
    blue_bg = np.array([0], dtype=np.uint8)
    result_img_data = np.full_like(img_data, blue_bg, dtype=np.uint8)

    for color in preserve_palette_colors:
        mask = (img_data == color)
        result_img_data[mask] = color  # Paste same color into mask

    for color in cc1_palette_colors:
        color_mask = (img_data == color)
        result_img_data[color_mask] = cc1_mask_color  # Paste cc1 mask color into mask

    for color in cc2_palette_colors:
        color_mask = (img_data == color)
        result_img_data[color_mask] = cc2_mask_color  # Paste cc1 mask color into mask

    # Convert the result back to an image
    result_img = Image.fromarray(result_img_data, mode="P")
    result_img.putpalette(data=PALETTE)

    mask_path = input_image_path + "--mask.png"
    # Save the resulting image
    result_img.save(mask_path)
    print(f"Processed mask saved to {mask_path}")

    bpp_img = img.convert('RGBA')
    bpp_img_data = np.array(bpp_img)
    for color in transparent_colors:
        mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)  # Find pixels that match the color
        bpp_img_data[mask] = (0, 0, 0, 0)  # Set them to fully transparent

    # Desaturate the cc1_colors
    for cc_color in cc1_colors + cc2_colors:
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
