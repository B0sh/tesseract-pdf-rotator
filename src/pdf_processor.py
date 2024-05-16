import fitz
import cv2
import numpy as np
import pytesseract
import re

class PDFProcessor:
    def __init__(self, input_pdf_path, output_pdf_path, remove_blank_pages=False):
        self.input_pdf_path = input_pdf_path
        self.output_pdf_path = output_pdf_path
        self.remove_blank_pages = remove_blank_pages

    def detect_orientation(self, image):
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            gray = cv2.medianBlur(gray, 3)
            osd = pytesseract.image_to_osd(gray)
            angle = int(re.search(r'(?<=Rotate: )\d+', osd).group(0))
            return angle
        except pytesseract.TesseractError as e:
            print(f"Error detecting orientation: {e}")
            return None  # Return None if detection fails
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def rotate_page(self, page, angle):
        if angle in [0, 90, 180, 270]:
            page.set_rotation(angle)

    def process_page(self, document, page_num):
        page = document.load_page(page_num)
        pix = page.get_pixmap(dpi=300)
        image = cv2.imdecode(np.frombuffer(pix.tobytes("png"), np.uint8), cv2.IMREAD_COLOR)
        angle = self.detect_orientation(image)
        
        if self.remove_blank_pages and angle is None:
            print(f"Skipping blank page: {page_num + 1}")
            return None
        
        if angle is not None:
            self.rotate_page(page, angle)
        
        return page

    def process_pdf(self, progress_callback=None):
        document = fitz.open(self.input_pdf_path)
        new_document = fitz.open()  # Create a new PDF document

        for page_num in range(len(document)):
            page = self.process_page(document, page_num)
            if page:
                new_document.insert_pdf(document, from_page=page.number, to_page=page.number)
            if progress_callback:
                progress_callback(page_num + 1, len(document))
        
        new_document.save(self.output_pdf_path)

        return {
            "total_pages_processed": len(document),
            "total_pages": len(new_document)
        }