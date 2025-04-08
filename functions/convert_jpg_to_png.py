from PIL import Image
import os

def convert(input_dir, output_dir):
    """Converts all JPG images in `input_dir` to PNG and saves them in `output_dir`."""
    if not os.path.exists(input_dir):
        raise FileNotFoundError("Input directory not found!")

    os.makedirs(output_dir, exist_ok=True)

    converted_files = []

    for file_name in os.listdir(input_dir):
        if file_name.lower().endswith(".jpg"):
            input_path = os.path.join(input_dir, file_name)
            output_name = file_name[:-4] + ".png"  # Change .jpg to .png
            output_path = os.path.join(output_dir, output_name)

            img = Image.open(input_path)
            img.convert("RGB").save(output_path, "PNG")
            converted_files.append(output_name)

    return converted_files
