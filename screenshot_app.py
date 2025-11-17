#!/usr/bin/env python3
"""
Script pour capturer un screenshot de l'interface Tube Effect
"""
import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap

# Import de la fenêtre principale
sys.path.insert(0, os.path.dirname(__file__))
# Importer directement depuis le fichier
import importlib.util
spec = importlib.util.spec_from_file_location("tube_effect", "Tube_Effect_1.2.py")
tube_effect = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tube_effect)
MainWindow = tube_effect.MainWindow

def capture_screenshot():
    """Capture un screenshot de l'application après son chargement"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    def take_screenshot():
        """Prend le screenshot après que l'interface soit chargée"""
        # Capturer la fenêtre
        pixmap = window.grab()
        pixmap.save("/home/user/Tube_Effect/interface_screenshot.png")
        print("✅ Screenshot sauvegardé : /home/user/Tube_Effect/interface_screenshot.png")
        app.quit()

    # Attendre 1 seconde que l'interface se charge, puis prendre le screenshot
    QTimer.singleShot(1000, take_screenshot)

    sys.exit(app.exec())

if __name__ == '__main__':
    capture_screenshot()
