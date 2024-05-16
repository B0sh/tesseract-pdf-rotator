import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QCheckBox, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt, pyqtSignal
from src.utilities import open_pdf

class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
        super().mousePressEvent(event)

class FileSelectorWidget(QWidget):
    file_selected = pyqtSignal(str, str, bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.file_select_label = ClickableLabel("Drag and drop a PDF file here\nor click to choose a file", self)
        self.file_select_label.setAlignment(Qt.AlignCenter)
        self.file_select_label.setStyleSheet("QLabel { border: 4px dashed #aaa; }")
        self.file_select_label.clicked.connect(self.open_file_dialog)
        self.setMinimumHeight(120)

        self.button = QPushButton("Process PDF", self)
        self.button.clicked.connect(self.select_output_file)
        self.button.setEnabled(False)

        self.remove_blank_pages_checkbox = QCheckBox("Remove Blank Pages", self)
        self.remove_blank_pages_checkbox.setChecked(True)
        self.remove_blank_pages_checkbox.stateChanged.connect(self.toggle_remove_blank_pages)

        self.results_label = QLabel("", self)
        self.results_label.setVisible(False)

        self.open_pdf_button = QPushButton("Open Processed PDF", self)
        self.open_pdf_button.clicked.connect(self.open_result_pdf)
        self.open_pdf_button.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.file_select_label)

        spacer = QSpacerItem(4, 4)
        layout.addItem(spacer)
        
        layout.addWidget(self.remove_blank_pages_checkbox)
        layout.addWidget(self.button)
        layout.addWidget(self.results_label)
        layout.addWidget(self.open_pdf_button)

        self.setLayout(layout)
        self.setAcceptDrops(True)

        self.reset()
        self.remove_blank_pages = True

    def reset(self):
        self.file_select_label.setText("Drag and drop a PDF file here\nor click to choose a file")
        self.button.setEnabled(False)
        self.input_pdf_path = None

    def show_last_result(self, result):
        self.last_result = result

        if self.remove_blank_pages:
            self.results_label.setText(f"Finished. Removed {result['total_blank_pages']} blank pages.")
        else:
            self.results_label.setText(f"Finished.")

        self.results_label.setVisible(True)
        self.open_pdf_button.setVisible(True)

    def open_result_pdf(self):
        output_pdf = self.last_result['output_pdf_path']
        open_pdf(output_pdf)

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
        self.file_select_label.setText(f"Opened {os.path.basename(path)}")
        self.button.setEnabled(True)

    def select_output_file(self):
        options = QFileDialog.Options()
        
        input_dir, input_file = os.path.split(self.input_pdf_path)
        output_file_name = os.path.splitext(input_file)[0] + "-processed.pdf"
        default_output_path = os.path.join(input_dir, output_file_name)
        
        output_pdf_path, _ = QFileDialog.getSaveFileName(self, "Save Processed PDF", default_output_path, "PDF Files (*.pdf);;All Files (*)", options=options)
        
        if output_pdf_path:
            self.file_selected.emit(self.input_pdf_path, output_pdf_path, self.remove_blank_pages)

    def toggle_remove_blank_pages(self, state):
        self.remove_blank_pages = state == Qt.Checked