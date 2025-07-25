import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, QWidget, 
                             QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                             QPushButton, QComboBox, QSpinBox, QDialog, 
                             QMessageBox, QListWidget, QListWidgetItem, QAction)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from display_manager import EnhancedDisplayManager, DisplayConfig, DisplayPreset

class PresetManager:
    def __init__(self):
        self.presets_file = "display_presets.json"
        self.presets = self.load_presets()
    
    def load_presets(self):
        """Load presets from JSON file"""
        if os.path.exists(self.presets_file):
            try:
                with open(self.presets_file, 'r') as f:
                    data = json.load(f)
                    presets = {}
                    for name, preset_data in data.items():
                        displays = []
                        for display_data in preset_data['displays']:
                            config = DisplayConfig(
                                device_name=display_data['device_name'],
                                resolution=tuple(display_data['resolution']),
                                refresh_rate=display_data['refresh_rate'],
                                position=tuple(display_data['position']),
                                orientation=display_data['orientation'],
                                scale=display_data['scale']
                            )
                            displays.append(config)
                        presets[name] = DisplayPreset(name, displays)
                    return presets
            except Exception as e:
                print(f"Error loading presets: {e}")
        return {}
    
    def save_presets(self):
        """Save presets to JSON file"""
        data = {}
        for name, preset in self.presets.items():
            displays_data = []
            for display in preset.displays:
                displays_data.append({
                    'device_name': display.device_name,
                    'resolution': list(display.resolution),
                    'refresh_rate': display.refresh_rate,
                    'position': list(display.position),
                    'orientation': display.orientation,
                    'scale': display.scale
                })
            data[name] = {'displays': displays_data}
        
        try:
            with open(self.presets_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving presets: {e}")
    
    def add_preset(self, name, displays):
        """Add a new preset"""
        self.presets[name] = DisplayPreset(name, displays)
        self.save_presets()
    
    def delete_preset(self, name):
        """Delete a preset"""
        if name in self.presets:
            del self.presets[name]
            self.save_presets()
    
    def get_preset_names(self):
        """Get list of preset names"""
        return list(self.presets.keys())

class SavePresetDialog(QDialog):
    def __init__(self, display_manager, parent=None):
        super().__init__(parent)
        self.display_manager = display_manager
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        self.setWindowTitle("Save Display Preset")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        # Preset name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Preset Name:"))
        self.name_edit = QLineEdit()
        name_layout.addWidget(self.name_edit)
        layout.addLayout(name_layout)
        
        # Display settings list
        self.displays_list = QListWidget()
        layout.addWidget(QLabel("Current Display Settings:"))
        layout.addWidget(self.displays_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save Preset")
        cancel_button = QPushButton("Cancel")
        
        save_button.clicked.connect(self.save_preset)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def load_current_settings(self):
        """Load and display current display settings"""
        displays = self.display_manager.get_display_devices()
        for device_name in displays:
            config = self.display_manager.get_display_settings(device_name)
            if config:
                item_text = f"{device_name}: {config.resolution[0]}x{config.resolution[1]} @ {config.refresh_rate}Hz"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, config)
                self.displays_list.addItem(item)
    
    def save_preset(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "Error", "Please enter a preset name.")
            return
        
        # Collect current display configurations
        displays = []
        for i in range(self.displays_list.count()):
            item = self.displays_list.item(i)
            config = item.data(Qt.UserRole)
            if config:
                displays.append(config)
        
        if displays:
            self.preset_name = name
            self.preset_displays = displays
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "No display settings to save.")

class DeletePresetDialog(QDialog):
    def __init__(self, preset_names, parent=None):
        super().__init__(parent)
        self.preset_names = preset_names
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Delete Preset")
        self.setModal(True)
        self.resize(300, 200)
        
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("Select preset to delete:"))
        
        self.preset_list = QListWidget()
        for name in self.preset_names:
            self.preset_list.addItem(name)
        layout.addWidget(self.preset_list)
        
        button_layout = QHBoxLayout()
        delete_button = QPushButton("Delete")
        cancel_button = QPushButton("Cancel")
        
        delete_button.clicked.connect(self.delete_preset)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(delete_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def delete_preset(self):
        current_item = self.preset_list.currentItem()
        if current_item:
            self.selected_preset = current_item.text()
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please select a preset to delete.")

class DisplayPresetsApp(QWidget):
    def __init__(self):
        super().__init__()
        self.display_manager = EnhancedDisplayManager()
        self.preset_manager = PresetManager()
        self.setup_system_tray()
    
    def setup_system_tray(self):
        """Setup the system tray icon and menu"""
        self.tray_icon = QSystemTrayIcon(self)
        
        # Create a simple icon
        from PyQt5.QtGui import QPixmap, QPainter, QColor
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor(0, 120, 215))  # Windows blue color
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(0, 0, 16, 16, Qt.AlignCenter, "D")
        painter.end()
        icon = QIcon(pixmap)
        self.tray_icon.setIcon(icon)
        
        # Create the tray menu
        self.tray_menu = QMenu()
        
        # Save preset action
        save_action = QAction("Save Current Display Preset", self)
        save_action.triggered.connect(self.save_current_preset)
        self.tray_menu.addAction(save_action)
        
        self.tray_menu.addSeparator()
        
        # Add preset actions dynamically
        self.preset_actions = {}
        self.update_preset_menu()
        
        self.tray_menu.addSeparator()
        
        # Delete preset action
        delete_action = QAction("Delete Preset", self)
        delete_action.triggered.connect(self.delete_preset)
        self.tray_menu.addAction(delete_action)
        
        self.tray_menu.addSeparator()
        
        # Open display settings action
        settings_action = QAction("Open Display Settings", self)
        settings_action.triggered.connect(self.open_display_settings)
        self.tray_menu.addAction(settings_action)
        
        self.tray_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        self.tray_menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Make sure the tray icon is visible
        if not self.tray_icon.isSystemTrayAvailable():
            print("System tray is not available!")
            return
            
        self.tray_icon.show()
        
        # Show a message to confirm it's working
        self.tray_icon.showMessage("Display Presets", 
                                  "App is running in system tray", 
                                  QSystemTrayIcon.Information, 3000)
    
    def update_preset_menu(self):
        """Update the preset menu items"""
        # Remove existing preset actions
        for action in self.preset_actions.values():
            self.tray_menu.removeAction(action)
        self.preset_actions.clear()
        
        # Add current presets
        preset_names = self.preset_manager.get_preset_names()
        for name in preset_names:
            action = QAction(name, self)
            action.triggered.connect(lambda checked, n=name: self.apply_preset(n))
            self.preset_actions[name] = action
            self.tray_menu.insertAction(self.tray_menu.actions()[1], action)
    
    def save_current_preset(self):
        """Save current display configuration as a preset"""
        dialog = SavePresetDialog(self.display_manager, self)
        if dialog.exec_() == QDialog.Accepted:
            self.preset_manager.add_preset(dialog.preset_name, dialog.preset_displays)
            self.update_preset_menu()
            self.tray_icon.showMessage("Display Presets", 
                                     f"Preset '{dialog.preset_name}' saved successfully!")
    
    def apply_preset(self, preset_name):
        """Apply a saved preset"""
        if preset_name in self.preset_manager.presets:
            preset = self.preset_manager.presets[preset_name]
            success_count = 0
            
            for display_config in preset.displays:
                if self.display_manager.apply_display_settings(display_config):
                    success_count += 1
            
            if success_count > 0:
                self.tray_icon.showMessage("Display Presets", 
                                         f"Applied preset '{preset_name}' to {success_count} display(s)")
            else:
                self.tray_icon.showMessage("Display Presets", 
                                         f"Failed to apply preset '{preset_name}'")
    
    def delete_preset(self):
        """Delete a saved preset"""
        preset_names = self.preset_manager.get_preset_names()
        if not preset_names:
            QMessageBox.information(self, "No Presets", "No presets to delete.")
            return
        
        dialog = DeletePresetDialog(preset_names, self)
        if dialog.exec_() == QDialog.Accepted:
            self.preset_manager.delete_preset(dialog.selected_preset)
            self.update_preset_menu()
            self.tray_icon.showMessage("Display Presets", 
                                     f"Preset '{dialog.selected_preset}' deleted successfully!")
    
    def open_display_settings(self):
        """Open Windows display settings"""
        self.display_manager.open_display_settings()
        self.tray_icon.showMessage("Display Presets", 
                                  "Display settings opened. You can manually adjust positions there.")
    
    def closeEvent(self, event):
        """Handle application close event"""
        self.tray_icon.hide()
        event.accept()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    
    # Create and show the main application
    window = DisplayPresetsApp()
    
    # Keep the app running
    sys.exit(app.exec_())

if __name__ == "__main__":
    main() 