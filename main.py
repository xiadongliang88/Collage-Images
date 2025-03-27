from PIL import Image, ImageDraw, ImageFont
import os
import math
import random
from conf import TARGET_TEXT, SMALL_IMAGES_DIR, OUTPUT_PATH, OUTPUT_SIZE, SMALL_IMG_SIZE, FONT_PATH, FONT_SIZE


def resize_with_crop(img, target_size):
    """Resize an image with cropping to match the target aspect ratio."""
    width, height = img.size
    target_width, target_height = target_size
    aspect = target_width / target_height

    if width / height > aspect:
        new_width = int(height * aspect)
        left = (width - new_width) // 2
        img = img.crop((left, 0, left + new_width, height))
    else:
        new_height = int(width / aspect)
        top = (height - new_height) // 2
        img = img.crop((0, top, width, top + new_height))

    return img.resize(target_size, Image.Resampling.LANCZOS)


def load_small_images(directory, target_size):
    """Load and resize small images from a directory."""
    small_images = []
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                img = Image.open(os.path.join(directory, filename))
                img = resize_with_crop(img, target_size)
                small_images.append(img)
            except Exception as e:
                print(f"Failed to load image: {filename}, Error: {e}")
    return small_images


def create_text_image(text, output_size, font_path=FONT_PATH, font_size=FONT_SIZE):
    """Create a grayscale image with the target text."""
    temp_img = Image.new('L', output_size, 0)
    draw = ImageDraw.Draw(temp_img)

    font = load_font(font_path, font_size)
    bbox = draw.textbbox((0, 0), text, font=font, anchor="lt")

    text_x = (output_size[0] - (bbox[2] - bbox[0])) // 2
    text_y = (output_size[1] - (bbox[3] - bbox[1])) // 2

    draw.text((text_x, text_y), text, fill=255, font=font)
    return temp_img


def load_font(font_path, font_size):
    """Load a font, falling back to default if unavailable."""
    try:
        return ImageFont.truetype(font_path or "simhei.ttf", font_size)
    except:
        try:
            return ImageFont.truetype("msyh.ttc", font_size)
        except:
            print("Warning: No Chinese font found, text may not display correctly")
            return ImageFont.load_default()


def paste_small_images(small_images, rows, cols, small_img_size, temp_img, output_img):
    """Paste small images onto the output image based on the text mask."""
    for y in range(rows):
        for x in range(cols):
            box = (
                x * small_img_size[0],
                y * small_img_size[1],
                (x + 1) * small_img_size[0],
                (y + 1) * small_img_size[1]
            )
            sample_x = box[0] + small_img_size[0] // 2
            sample_y = box[1] + small_img_size[1] // 2

            if sample_x < temp_img.width and sample_y < temp_img.height:
                small_img = random.choice(small_images)
                small_img = prepare_small_image(small_img, box, temp_img.getpixel((sample_x, sample_y)))
                output_img.paste(small_img, box, small_img if small_img.mode == "RGBA" else None)


def prepare_small_image(small_img, box, pixel_value):
    """Prepare a small image for pasting, applying transparency if needed."""
    small_img = small_img.resize((box[2] - box[0], box[3] - box[1]))
    if pixel_value <= 128:
        small_img = small_img.convert("RGBA")
        alpha = small_img.split()[3].point(lambda p: p * 0.6)
        small_img.putalpha(alpha)
    return small_img


def create_character_mosaic(target_text, small_images_dir, output_path, output_size=(7680, 4320), small_img_size=(60, 60)):
    """Main function to create a character mosaic."""
    small_images = load_small_images(small_images_dir, (100, 100))
    if not small_images:
        raise ValueError("No usable images found")

    temp_img = create_text_image(target_text, output_size)
    cols = math.ceil(output_size[0] / small_img_size[0])
    rows = math.ceil(output_size[1] / small_img_size[1])

    output_img = Image.new('RGB', (cols * small_img_size[0], rows * small_img_size[1]))
    paste_small_images(small_images, rows, cols, small_img_size, temp_img, output_img)

    output_img.save(output_path)
    print(f"Image saved to: {output_path}")


if __name__ == "__main__":
    target_text = "WIN"
    small_images_dir = "images"
    output_path = "youbang_poster.jpg"

    if not os.path.exists(small_images_dir):
        os.makedirs(small_images_dir)
        print(f"Please place small images in the {small_images_dir} directory")
    else:
        create_character_mosaic(
            target_text=TARGET_TEXT,
            small_images_dir=SMALL_IMAGES_DIR,
            output_path=OUTPUT_PATH,
            output_size=OUTPUT_SIZE,
            small_img_size=SMALL_IMG_SIZE
        )