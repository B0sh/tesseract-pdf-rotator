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
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def rotate_page(page, angle):
    if angle is not None:
        rotation = {0: 0, 90: 90, 180: 180, 270: 270}
        if angle in rotation:
            page.set_rotation(rotation[angle])

def process_pdf(input_pdf_path, output_pdf_path, remove_blank_pages=False):
    document = fitz.open(input_pdf_path)
    new_document = fitz.open()  # Create a new PDF document
    for page_num in range(len(document)):
        print(f"Processing page: {page_num + 1} / {len(document)}")
        page = document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        image = cv2.imdecode(np.frombuffer(pix.tobytes("png"), np.uint8), cv2.IMREAD_COLOR)
        angle = detect_orientation(image)
        
        if remove_blank_pages and angle is None:
            print(f"Skipping blank page: {page_num + 1}")
            continue  # Skip blank pages
        
        if angle is not None:
            rotate_page(page, angle)
        
        new_document.insert_pdf(document, from_page=page_num, to_page=page_num)
    
    new_document.save(output_pdf_path)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: main.py input.pdf output.pdf [remove_blank_pages]")
    else:
        input_pdf = sys.argv[1]
        output_pdf = sys.argv[2]
        remove_blank_pages = bool(int(sys.argv[3])) if len(sys.argv) > 3 else False
        process_pdf(input_pdf, output_pdf, remove_blank_pages)