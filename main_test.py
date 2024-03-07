import sys
import os
import os.path
import pymol
cmd = pymol.cmd
import subprocess
import networkx as nx
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QWidget, QProgressBar
from run_api import run
from centrality_analysis import generate_graph
from pymol_viz import transform_csv
# from pairwise_regression import thisIsBetter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Submitting files to RING")
        self.setGeometry(400, 400, 800, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)  # Set central widget for QMainWindow
        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        self.progressBar = QProgressBar()

        self.start_button = QPushButton("Start API", self)
        self.start_button.clicked.connect(self.runAPI)
        self.start_button.setGeometry(50, 50, 200, 50)
        # layout.addWidget(self.start_button)

        self.analysis_button = QPushButton("Start Ananlysis", self)
        self.analysis_button.clicked.connect(self.runAnalysis)
        self.analysis_button.setGeometry(50, 85, 200, 50)

        self.visualization_button = QPushButton("Start Visualization", self)
        self.visualization_button.clicked.connect(self.runVisual)
        self.visualization_button.setGeometry(50, 120, 200, 50)

        self.start_button = QPushButton("Start PyMOL", self)
        self.start_button.clicked.connect(self.startPymol)
        self.start_button.setGeometry(50, 155, 200, 50)

        self.stop_button = QPushButton("Stop PyMOL", self)
        self.stop_button.clicked.connect(self.stopPymol)
        self.stop_button.setGeometry(50, 190, 200, 50)

        self.dash_button = QPushButton("Start App", self)
        self.dash_button.clicked.connect(self.runApp)
        self.dash_button.setGeometry(50, 225, 200, 50)

        self.pymol_initialized = False

        self.setLayout(layout)

    def get_current_run_config(self):
        edge_policy = "--best_edge"
            
        seq_sep = '3'
        len_hbond = '5.5'
        len_pica = '7.0'
        len_pipi = '7.0'
        len_salt = '5.0'
        len_ss = '3.0'
        len_vdw = '0.8'

        return {
            "-g": seq_sep,
            "-o": len_salt,
            "-s": len_ss,
            "-k": len_pipi,
            "-a": len_pica,
            "-b": len_hbond,
            "-w": len_vdw,
            "edges": edge_policy
        }

    def runAPI(self):
        file_dialog = QFileDialog(self)  # Set parent widget for file dialog
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.text_edit.setPlainText(file_contents)

        file = os.path.basename(file_path)
        dir_path = os.path.dirname(file_path)

        current_config = self.get_current_run_config()
        run(file, file_path, current_config, dir_path, self.progress)
        self.progressBar = QProgressBar(self)
        self.progressBar.setRange(0, 100) 

    def runAnalysis(self):
        file_dialog = QFileDialog(self)  # Set parent widget for file dialog
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.text_edit.setPlainText(file_contents)

        generate_graph(file_path)

    def runVisual(self):
        file_dialog = QFileDialog(self)  # Set parent widget for file dialog
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.text_edit.setPlainText(file_contents)

        transform_csv(file_path)

    def startPymol(self):
        # Start PyMOL subprocess
        self.pymol_process = subprocess.Popen(['pymol'])

    def stopPymol(self):
        # Stop PyMOL subprocess if it's running
        if self.pymol_process and self.pymol_process.poll() is None:
            self.pymol_process.terminate()

        

    def runApp(self):
        file_dialog = QFileDialog(self)  # Set parent widget for file dialog
        file_path, _ = file_dialog.getOpenFileName(self, "Open File", "", "All Files (*)")

        if file_path:
            with open(file_path, 'r') as file:
                file_contents = file.read()
                self.text_edit.setPlainText(file_contents)

        thisIsBetter(file_path)
            

    def progress(self, p):
        if not self.progressBar.isVisible():
            self.progressBar.setVisible(True)
        self.progressBar.setValue(int(p))
        self.progressBar.setFormat("%.02f %%" % p)
        QApplication.instance().processEvents()  # Use QApplication.instance() directly here

    def close_progress(self):
        if self.process_completed:
            self.progressBar.setVisible(False)  # Hide the progress bar
            self.close_button.setVisible(False)  # Hide the close button
            self.process_completed = False  # Reset the completion flag


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show() 
    sys.exit(app.exec())
