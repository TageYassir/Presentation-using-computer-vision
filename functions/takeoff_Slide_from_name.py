import os
from PIL import Image

def rename_images(image_dir, output_dir):
    """Removes the first 5 characters from PNG filenames and saves them in `output_dir`."""
    if not os.path.exists(image_dir):
        raise FileNotFoundError("Image directory not found!")

    os.makedirs(output_dir, exist_ok=True)

    renamed_files = []

    for file_name in os.listdir(image_dir):
        if file_name.lower().endswith(".png"):  # Check if it's a PNG image
            number_part = file_name[5:-4]  # Remove first 5 characters and ".png"

            if number_part.isdigit():
                new_name = f"{number_part}.png"
                input_path = os.path.join(image_dir, file_name)
                output_path = os.path.join(output_dir, new_name)

                img = Image.open(input_path)
                img.save(output_path)
                renamed_files.append(new_name)

    return renamed_files
