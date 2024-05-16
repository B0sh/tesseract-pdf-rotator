import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from src.file_selector_widget import FileSelectorWidget
from src.processing_widget import ProcessingWidget


class PDFProcessorApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.file_selector = FileSelectorWidget(self)
        self.processing_screen = ProcessingWidget(self)

        self.addWidget(self.file_selector)
        self.addWidget(self.processing_screen)

        self.file_selector.file_selected.connect(self.on_pdf_file_selected)
        self.processing_screen.processing_finished.connect(self.on_pdf_finished_processing)

        self.resize(400, 200)

    def on_pdf_file_selected(self, input_pdf_path, output_pdf_path, remove_blank_pages):
        self.setCurrentWidget(self.processing_screen)
        self.processing_screen.start_processing(input_pdf_path, output_pdf_path, remove_blank_pages)

    def on_pdf_finished_processing(self):
        self.setCurrentWidget(self.file_selector)
        self.file_selector.reset()