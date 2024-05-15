import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog, QProgressBar
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from pdf_processor import PDFProcessor

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

class PDFProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_pdf_path = ""
        self.output_pdf_path = ""

    def initUI(self):
        self.setWindowTitle("PDF Processor")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Drag and drop a PDF file here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 4px dashed #aaa; }")

        self.button = QPushButton("Process PDF", self)
        self.button.clicked.connect(self.process_pdf)
        self.button.setEnabled(False)

        self.progress = QProgressBar(self)
        self.progress.setValue(0)
        self.progress.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.progress)

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
            self.label.setText(f"Opened {os.path.basename(self.input_pdf_path)}")
            self.button.setEnabled(True)

    def process_pdf(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save Processed PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        
        if output_pdf_path:
            self.output_pdf_path = output_pdf_path
            self.thread = PDFProcessorThread(self.input_pdf_path, self.output_pdf_path, remove_blank_pages=True)
            self.thread.progress.connect(self.update_progress)
            self.thread.start()

    def update_progress(self, current, total):
        self.progress.setMaximum(total)
        self.progress.setValue(current)
        if current == total:
            self.label.setText(f"Processed PDF saved!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PDFProcessorApp()
    ex.show()
    sys.exit(app.exec_())