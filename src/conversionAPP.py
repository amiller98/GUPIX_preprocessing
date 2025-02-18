import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QProgressBar, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from converter import MCAtoOxfordConverter 


class Worker(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    
    def __init__(self, folder_path):
        super(Worker, self).__init__()
        self.folder_path = folder_path

    def run(self):
        converter = MCAtoOxfordConverter(self.folder_path)
        converter.convert_folder()
        converter.find_dat_files(self.folder_path)
        self.finished.emit()


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('MCA for GUPIX')
        
        layout = QVBoxLayout()

        self.folder_edit = QLineEdit(self)
        self.folder_edit.setPlaceholderText('Enter folder path...')
        layout.addWidget(self.folder_edit)

        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_conversion)
        layout.addWidget(self.run_button)

        self.setLayout(layout)
        self.show()

    def run_conversion(self):
        folder_path = self.folder_edit.text()
        self.run_button.setEnabled(False)
        self.worker = Worker(folder_path)
        self.worker.finished.connect(self.on_finished) 
        self.worker.start()

    def on_finished(self):
        self.run_button.setEnabled(True)
        QMessageBox.information(self, 'Conversion Complete', 'The conversion is done!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
