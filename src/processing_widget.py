from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt
from src.pdf_processor import PDFProcessor
from PyQt5.QtCore import QThread, pyqtSignal

class PDFProcessorThread(QThread):
    progress = pyqtSignal(int, int)  # Current progress, total progress

    def __init__(self, input_pdf_path, output_pdf_path, remove_blank_pages):
        super().__init__()
        self.input_pdf_path = input_pdf_path
        self.output_pdf_path = output_pdf_path
        self.remove_blank_pages = remove_blank_pages

    def run(self):
        processor = PDFProcessor(self.input_pdf_path, self.output_pdf_path, self.remove_blank_pages)
        processor.process_pdf(self.update_progress)

    def update_progress(self, current, total):
        self.progress.emit(current, total)

class ProcessingWidget(QWidget):
    processing_finished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Processor - Processing")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Creating PDF Images", self)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.progress)

        self.setLayout(layout)

    def start_processing(self, input_pdf_path, output_pdf_path, remove_blank_pages):
        self.thread = PDFProcessorThread(input_pdf_path, output_pdf_path, remove_blank_pages)
        self.thread.progress.connect(self.update_progress)
        self.thread.start()

    def update_progress(self, current, total):
        self.label.setText("Scanning Page %d of %d" % (current, total))
        self.progress.setMaximum(total)
        self.progress.setValue(current)

        if current == total:
            self.finish_processing()

    def finish_processing(self):
        self.processing_finished.emit()