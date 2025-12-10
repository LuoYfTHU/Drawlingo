#!/usr/bin/env python3
"""
Drawlingo - Sketch-Based Language Learning App
Python version using PyQt6
"""

import sys
from PyQt6.QtWidgets import QApplication
from MainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    
    app.setApplicationName("Drawlingo")
    app.setApplicationVersion("2.0.0")
    app.setOrganizationName("Drawlingo")
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

