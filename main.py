import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.app import PDFProcessorApp
import pytesseract

def show_error_message(message):
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(message)
    msg_box.setWindowTitle("Error")
    msg_box.exec_()
    sys.exit(1)

# Determine if the script is running as a PyInstaller bundle
if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
else:
    bundle_dir = os.path.dirname(os.path.abspath(__file__))
tesseract_executable = os.path.join(bundle_dir, 'tesseract')
tessdata_dir = os.path.join(bundle_dir, 'tessdata')

if not os.path.exists(tesseract_executable):
    show_error_message(f"Tesseract executable not found: {tesseract_executable}")

if not os.path.exists(tessdata_dir):
    show_error_message(f"Tessdata directory not found: {tessdata_dir}")

os.environ['TESSDATA_PREFIX'] = tessdata_dir
pytesseract.pytesseract.tesseract_cmd = tesseract_executable

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())