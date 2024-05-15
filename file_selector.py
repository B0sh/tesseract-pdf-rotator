import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal

class FileSelector(QWidget):
    file_selected = pyqtSignal(str, str)  # Input path, Output path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Processor - Select File")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Drag and drop a PDF file here", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 4px dashed #aaa; }")

        self.button = QPushButton("Next", self)
        self.button.clicked.connect(self.select_output_file)
        self.button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)
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

    def select_output_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save Processed PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if output_pdf_path:
            self.file_selected.emit(self.input_pdf_path, output_pdf_path)