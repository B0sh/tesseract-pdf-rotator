import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from file_selector import FileSelector
from processing_screen import ProcessingScreen

class PDFProcessorApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_selector = FileSelector(self)
        self.processing_screen = ProcessingScreen(self)

        self.addWidget(self.file_selector)
        self.addWidget(self.processing_screen)

        self.file_selector.file_selected.connect(self.start_processing)

    def start_processing(self, input_pdf_path, output_pdf_path):
        self.setCurrentWidget(self.processing_screen)
        self.processing_screen.start_processing(input_pdf_path, output_pdf_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())