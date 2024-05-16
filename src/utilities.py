import os
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

def open_pdf(output_pdf):
    try:
        if os.name == 'nt':  # Windows
            os.startfile(output_pdf)
        elif os.name == 'posix':  # macOS or Linux
            os.system(f'open "{output_pdf}"' if sys.platform == 'darwin' else f'xdg-open "{output_pdf}"')
    except Exception as e:
        print(f"Failed to open file: {e}")

def show_error_message(message):
    app = QApplication(sys.argv)
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(message)
    msg_box.setWindowTitle("Error")
    msg_box.exec_()
    sys.exit(1)

