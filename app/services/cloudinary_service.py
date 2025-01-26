import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import os

load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET")
)

def upload_image_to_cloudinary(file):
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(file.file)
        return result["secure_url"]  # Returns the URL of the uploaded image
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None