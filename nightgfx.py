from PIL import Image
import numpy as np


# Function to desaturate a color
def desaturate_color(color):
    avg = int(np.mean(color))  # Calculate the average of the RGB values
    return avg, avg, avg  # Return the desaturated color


def process_image_pil(input_image, automatic_lights=None):
    img = input_image

    PALETTE = img.getpalette()
    def palette_to_rgb(color_index):
        return PALETTE[color_index * 3: color_index * 3 + 3]

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

    light_colors = {64: 68, 65: 68, 66: 69, 67: 69, 68: 69, 69: 69}

    window_colors = {128: 64, 129: 65, 130: 66, 131: 67, 132: 67, 133: 68, 134: 68, 135: 69}

    red_light_colors = [182, 183, 184]

    window_rgb_colors = []
    for color, new_color in window_colors.items():
        window_rgb_color = palette_to_rgb(color)
        light_rgb_color = palette_to_rgb(new_color)
        window_rgb_colors.append([tuple(window_rgb_color), tuple(light_rgb_color)])

    light_rgb_colors = []
    for color, new_color in light_colors.items():
        a_color = palette_to_rgb(color)
        b_color = palette_to_rgb(new_color)
        light_rgb_colors.append([tuple(a_color), tuple(b_color)])

    red_rgb_colors = []
    for color in red_light_colors:
        red_rgb_colors.append(tuple(palette_to_rgb(color)))

    preserve_rgb_colors = []
    for color in preserve_palette_colors:
        preserve_rgb_colors.append(tuple(palette_to_rgb(color)))

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

    if automatic_lights:
        for color, new_color in light_colors.items():
            color_mask = (img_data == color)
            result_img_data[color_mask] = new_color

    # Convert the result back to an image
    result_img = Image.fromarray(result_img_data, mode="P")
    result_img.putpalette(data=PALETTE)

    print(f"Created mask")

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

    light_masks = []
    window_masks = []
    red_masks = []
    preserve_masks = []
    if automatic_lights:
        for color, new_color in light_rgb_colors:
            mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)
            light_masks.append([mask, color, new_color])
        for color, new_color in window_rgb_colors:
            mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)
            window_masks.append([mask, color, new_color])
        for color in red_rgb_colors:
            mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)
            red_masks.append([mask, color])
        for color in preserve_rgb_colors:
            mask = np.all(bpp_img_data[:, :, :3] == color, axis=-1)
            preserve_masks.append([mask, color])

    bpp_result_img = Image.fromarray(bpp_img_data)
    if automatic_lights:
        black_overlay = Image.new("RGBA", bpp_result_img.size, (0, 0, 0, int(255 * 0.65)))
        bpp_result_img = Image.alpha_composite(bpp_result_img, black_overlay)
        bpp_img_data = np.array(bpp_result_img)
        mask = np.all(bpp_img_data == (0, 0, 0, int(255 * 0.65)), axis=-1)
        bpp_img_data[mask] = (0, 0, 0, 0)  # Set them to fully transparent
        brightness = 0.75
        for mask, color, new_color in window_masks:
            bpp_img_data[mask, :3] = (new_color[0] * brightness, new_color[1] * brightness, new_color[2] * brightness)
        for mask, color, new_color in light_masks:
            bpp_img_data[mask, :3] = new_color
        for mask, new_color in red_masks:
            bpp_img_data[mask, :3] = new_color
        for mask, new_color in preserve_masks:
            bpp_img_data[mask, :3] = new_color
        bpp_result_img = Image.fromarray(bpp_img_data)

    print(f"Created 32bpp night image")
    return result_img, bpp_result_img

def process_image(input_image_path, automatic_lights=None, output_mask_path=None, output_image_path=None,):
    # Open the input image
    if input_image_path[-4:].lower() == ".png":
        input_image_path = input_image_path[:-4]
    img = Image.open(input_image_path + ".png")

    mask_result_img, bpp_result_img, = process_image_pil(img, automatic_lights)

    if output_mask_path is None:
        output_mask_path = input_image_path + "--mask.png"
    # Save the resulting image
    mask_result_img.save(output_mask_path)
    print(f"Processed mask saved to {output_mask_path}")
    if output_image_path is None:
        output_image_path = input_image_path + "--32bpp.png"
    bpp_result_img.save(output_image_path)
    print(f"Processed 32bpp saved to {output_image_path}")
