#!/usr/bin/env python3
"""
Simple test to verify system tray functionality
"""

import sys
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

def create_icon():
    """Create a simple icon"""
    pixmap = QPixmap(16, 16)
    pixmap.fill(QColor(0, 120, 215))  # Windows blue
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 255))
    painter.drawText(0, 0, 16, 16, Qt.AlignCenter, "D")
    painter.end()
    return QIcon(pixmap)

def main():
    app = QApplication(sys.argv)
    
    # Check if system tray is available
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available!")
        return
    
    # Create tray icon
    tray = QSystemTrayIcon()
    tray.setIcon(create_icon())
    
    # Create menu
    menu = QMenu()
    test_action = QAction("Test Action", menu)
    test_action.triggered.connect(lambda: print("Test action clicked!"))
    menu.addAction(test_action)
    
    exit_action = QAction("Exit", menu)
    exit_action.triggered.connect(app.quit)
    menu.addAction(exit_action)
    
    tray.setContextMenu(menu)
    tray.show()
    
    # Show message
    tray.showMessage("Test", "System tray test is working!", 
                    QSystemTrayIcon.Information, 3000)
    
    print("System tray test is running. Look for the blue 'D' icon in your system tray.")
    print("Right-click it to see the menu.")
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 