import shutil
import pytesseract

# Find the tesseract executable path
tesseract_path = shutil.which('tesseract')

if tesseract_path is None:
    raise EnvironmentError("Tesseract not found. Ensure Tesseract is installed and available in your PATH.")

# Set the tesseract executable path in pytesseract
print(tesseract_path)

# Example usage
# try:
#     # Your image processing code here
#     text = pytesseract.image_to_string('example_image.png')
#     print(text)
# except Exception as e:
#     print(f"An error occurred: {e}")