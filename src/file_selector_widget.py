import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt5.QtCore import Qt, pyqtSignal

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class FileSelectorWidget(QWidget):
    file_selected = pyqtSignal(str, str)  # Input path, Output path

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("PDF Processor - Select File")
        self.setGeometry(100, 100, 400, 200)

        self.label = ClickableLabel("Drag and drop a PDF file here\nor click to choose a file", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("QLabel { border: 4px dashed #aaa; }")
        self.label.clicked.connect(self.open_file_dialog)

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
            path = urls[0].toLocalFile()
            self.selectInputFile(path)

    def open_file_dialog(self):
        options = QFileDialog.Options()
        input_pdf_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if input_pdf_path:
            self.selectInputFile(input_pdf_path)

    def selectInputFile(self, path):
        self.input_pdf_path = path
        self.label.setText(f"Opened {os.path.basename(path)}")
        self.button.setEnabled(True)

    def select_output_file(self):
        options = QFileDialog.Options()
        output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save Processed PDF", "", "PDF Files (*.pdf);;All Files (*)", options=options)
        if output_pdf_path:
            self.file_selected.emit(self.input_pdf_path, output_pdf_path)