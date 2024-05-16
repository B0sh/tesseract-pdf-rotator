import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from src.app import PDFProcessorApp
from src.utilities import show_error_message
import pytesseract

def find_tesseract_resources():
    if getattr(sys, 'frozen', False):
        bundle_dir = sys._MEIPASS
    else:
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    tesseract_executable = os.path.join(os.path.join(bundle_dir, 'tesseract'), 'tesseract')
    tessdata_dir = os.path.join(bundle_dir, 'tessdata')


    # Check if tesseract executable and tessdata directory exist in the initial locations
    if not os.path.exists(tesseract_executable):
        bundle_dir = os.path.join(bundle_dir, 'dist/Walden PDF.app/Contents/Frameworks/')
        tesseract_executable = os.path.join(os.path.join(bundle_dir, 'tesseract'), 'tesseract')
        tessdata_dir = os.path.join(bundle_dir, 'tessdata')

    # Final check to ensure paths exist
    if not os.path.exists(tesseract_executable):
        show_error_message(f"Tesseract executable not found: {tesseract_executable}")
        return None, None

    if not os.path.exists(tessdata_dir):
        show_error_message(f"Tessdata directory not found: {tessdata_dir}")
        return None, None

    return tesseract_executable, tessdata_dir

def main():
    # Find the paths to tesseract and tessdata
    tesseract_executable, tessdata_dir = find_tesseract_resources()
    print(tesseract_executable, tessdata_dir)

    if tesseract_executable is None or tessdata_dir is None:
        sys.exit(1)

    os.environ['TESSDATA_PREFIX'] = tessdata_dir
    pytesseract.pytesseract.tesseract_cmd = tesseract_executable

    # Start the application
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()