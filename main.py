import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from src.app import PDFProcessorApp

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())