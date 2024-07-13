import requests
from PIL import Image
import os
import subprocess
from datetime import datetime

def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully!")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        print(response.text)

def crop_and_resize_image(input_image_path, output_image_path, output_size):
    try:
        with Image.open(input_image_path) as img:
            width, height = img.size
            target_width, target_height = output_size
            
            # Calculate cropping box to maintain aspect ratio
            aspect_ratio = target_width / target_height
            new_width = width
            new_height = int(new_width / aspect_ratio)
            
            if new_height > height:
                new_height = height
                new_width = int(new_height * aspect_ratio)
            
            left = (width - new_width) / 2
            top = 0  # Start from the top
            right = (width + new_width) / 2
            bottom = new_height
            
            img = img.crop((left, top, right, bottom))
            img = img.resize(output_size, Image.LANCZOS)
            img.save(output_image_path)
            print(f"Image saved as {output_image_path}")
    except Exception as e:
        print(f"Error processing image: {e}")

def set_wallpaper(image_path):
    image_path = os.path.abspath(image_path)
    script = f"""
    tell application "System Events"
        tell every desktop
            set picture to "{image_path}"
        end tell
    end tell
    """
    process = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
    if process.returncode == 0:
        print("Wallpaper set successfully on macOS!")
    else:
        print(f"Failed to set wallpaper. Error: {process.stderr}")

def generate_timestamp():
    now = datetime.utcnow()
    return now.strftime("%Y_%m_%d_%H_%M_%S")

# URL of the image (static URL)
url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/5424x5424.jpg"
download_path = "./current.jpg"
output_size = (3456, 2234)  # Updated to desired size

# Download the image
download_image(url, download_path)

# Print the first few bytes of the downloaded file for debugging
try:
    with open(download_path, "rb") as file:
        print(file.read(100))  # Print first 100 bytes
except Exception as e:
    print(f"Error reading downloaded file: {e}")

# Create output image name with formatted timestamp
timestamp = generate_timestamp()
output_image_name = f"wallpaper_{timestamp}.jpg"

# Process and save the image
crop_and_resize_image(download_path, output_image_name, output_size)

# Set the wallpaper
set_wallpaper(output_image_name)

# Log the execution
log_file_path = os.path.expanduser('~') + "/Desktop/wallpaper-scripts/execution_log.txt"
with open(log_file_path, "a") as log_file:
    log_file.write(f"Script executed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
