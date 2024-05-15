import fitz  # PyMuPDF
import cv2
import numpy as np
import pytesseract
import re

def detect_orientation(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)
        osd = pytesseract.image_to_osd(gray)
        angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))
        return angle
    except pytesseract.TesseractError as e:
        print(f"Error detecting orientation: {e}")
        return -1
    except Exception as e:
        print(f"Unexpected error: {e}")
        return -1

def rotate_page(page, angle):
    rotation = {0: 0, 90: 90, 180: 180, 270: 270}
    if angle in rotation:
        page.set_rotation(rotation[angle])

def process_pdf(input_pdf_path, output_pdf_path):
    document = fitz.open(input_pdf_path)
    for page_num in range(len(document)):
        print("Processing page", page_num)
        page = document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        image = cv2.imdecode(np.frombuffer(pix.tobytes("png"), np.uint8), cv2.IMREAD_COLOR)
        angle = detect_orientation(image)
        
        print(f"Detected orientation: {angle}")
        rotate_page(page, angle)
    document.save(output_pdf_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: main.py input.pdf output.pdf")
    else:
        process_pdf(sys.argv[1], sys.argv[2])