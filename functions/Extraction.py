import os
import zipfile

def extract_images(zip_file_path, output_dir):
    """Extracts image files from a ZIP archive."""
    if not os.path.exists(zip_file_path):
        raise FileNotFoundError("ZIP file not found!")

    os.makedirs(output_dir, exist_ok=True)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                zip_ref.extract(file_name, output_dir)
                print(f"Extracted: {file_name}")

    print(f"Extraction completed! Images saved in {output_dir}")
