# Display Preset Manager

A Windows system tray application that allows you to save and apply display configuration presets. The app manages resolution, refresh rate, orientation, and DPI scaling for all connected monitors.

## Features

- **Save Display Presets**: Capture current display settings for all connected monitors
- **Apply Presets**: Quickly switch between saved display configurations
- **System Tray Integration**: Runs in the background with easy access via system tray
- **Multi-Monitor Support**: Handles multiple displays with individual settings
- **Persistent Storage**: Presets are saved to JSON file and persist between sessions
- **Delete Presets**: Remove unwanted presets from the system

## Requirements

- Windows 11 (or Windows 10)
- Python 3.8 or higher
- Administrator privileges (required for display settings changes)

## Installation

### Option 1: PyPI Package
```bash
pip install display-preset-manager
display-preset-manager
```

### Option 2: From Source
1. **Clone or download the project files**
2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python display_presets.py
   ```

### Option 3: Standalone Executable
1. Download the latest release from GitHub
2. Run `DisplayPresetManager.exe` as administrator

## Usage

### Starting the App

1. Run the application as administrator (required for display settings changes)
2. The app will appear in the system tray with a display icon
3. Right-click the tray icon to access the menu

### Saving a Preset

1. Configure your displays to the desired settings (resolution, refresh rate, etc.)
2. Right-click the system tray icon
3. Select "Save Current Display Preset"
4. Enter a name for your preset
5. Click "Save Preset"

### Applying a Preset

1. Right-click the system tray icon
2. Select the preset name from the menu
3. The display settings will be applied immediately

### Deleting a Preset

1. Right-click the system tray icon
2. Select "Delete Preset"
3. Choose the preset to delete from the list
4. Click "Delete"

### Exiting the App

1. Right-click the system tray icon
2. Select "Exit"

## Display Settings Managed

- **Resolution**: Width and height in pixels
- **Refresh Rate**: Monitor refresh rate in Hz
- **Orientation**: Display rotation (0°, 90°, 180°, 270°)
- **DPI Scaling**: Display scaling percentage

## Preset Storage

Presets are stored in `display_presets.json` with the following structure:
```json
{
  "Preset Name": {
    "displays": [
      {
        "device_name": "\\\\.\\DISPLAY1",
        "resolution": [1920, 1080],
        "refresh_rate": 60,
        "orientation": 0,
        "scale": 100
      }
    ]
  }
}
```

## Troubleshooting

### Common Issues

1. **"Access Denied" errors**: Run the app as administrator
2. **Display settings not applying**: Ensure your graphics drivers support the requested settings
3. **App not appearing in system tray**: Check if system tray icons are hidden

### Administrator Rights

The application requires administrator privileges to modify display settings. If you encounter permission errors:

1. Right-click on the Python executable or command prompt
2. Select "Run as administrator"
3. Navigate to the project directory
4. Run `python display_presets.py`

## Development

### Building from Source

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python display_presets.py`

### Creating Executable

```bash
python build_exe.py
```

### Creating Installer

1. Install NSIS
2. Run: `makensis installer.nsi`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

If you encounter any issues or have questions, please open an issue on GitHub. 