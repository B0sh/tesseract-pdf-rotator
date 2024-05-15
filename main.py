import fitz  # PyMuPDF
import cv2
import numpy as np
import pytesseract
import re
import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5.QtCore import Qt

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

class PDFProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_pdf_path = ""
        self.output_pdf_path = ""

    def initUI(self):
        self.setWindowTitle("Walden's PDF Processor")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Drag and drop a PDF file here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 4px dashed #aaa; }")

        self.button = QPushButton("Process PDF", self)
        self.button.clicked.connect(self.process_pdf)
        self.button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            self.input_pdf_path = urls[0].toLocalFile()
            self.label.setText(f"File: {self.input_pdf_path}")
            self.button.setEnabled(True)

    def process_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save Processed PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if output_pdf_path:
            self.output_pdf_path = output_pdf_path
            process_pdf(self.input_pdf_path, self.output_pdf_path, remove_blank_pages=True)
            self.label.setText(f"Processed PDF saved to: {self.output_pdf_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())