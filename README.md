# air-caps-apk-update

Air-Caps Smart Glasses Rework Tool - A Windows desktop application for reworking Android-based smart glasses.

## Overview

This software is used in the rework process for a batch of smart glasses running Android. The tool provides a streamlined workflow for operators to:

1. Connect smart glasses to a Windows PC via a special cable
2. Scan QR codes to capture device serial numbers
3. Perform testing, APK uploading, and verification through a simple GUI

## Features

- **QR Code Serial Number Input**: Quick serial number entry via barcode scanner
- **Device Connection Monitoring**: Automatic detection of connected Android devices via ADB
- **Automated Testing**: Run comprehensive device tests including:
  - Device model verification
  - Battery status check
  - Storage capacity check
  - Installed packages verification
- **APK Upload**: Install/update applications on the smart glasses
- **Device Verification**: Validate device configuration and state
- **Activity Logging**: Real-time logging of all operations
- **Progress Indicators**: Visual feedback during operations

## Prerequisites

### Required Software

1. **Python 3.7 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Android SDK Platform Tools (ADB)**
   - Download from [Android Developer website](https://developer.android.com/studio/releases/platform-tools)
   - Extract to a folder (e.g., `C:\platform-tools`)
   - Add the folder to your system PATH

### Verifying ADB Installation

Open Command Prompt and run:
```cmd
adb version
```

You should see the ADB version information.

## Installation

1. Clone or download this repository:
```cmd
git clone https://github.com/smaohua/air-caps-apk-update.git
cd air-caps-apk-update
```

2. (Optional) Install additional packages for enhanced QR code scanning:
```cmd
pip install -r requirements.txt
```

## Usage

### Starting the Application

Run the application using Python:
```cmd
python main.py
```

### Workflow

1. **Connect the Device**
   - Connect the smart glasses to your PC using the special cable
   - The application will automatically detect the device
   - Wait for "Device Connected" status to show green

2. **Scan Serial Number**
   - Click in the "Scan QR Code" field
   - Use your QR code scanner to scan the device's QR code
   - The serial number will appear in the field
   - Press Enter or click elsewhere to confirm

3. **Run Tests**
   - Click "1. Run Tests" button
   - The application will perform automated tests on the device
   - Review the activity log for test results

4. **Upload APK**
   - Ensure the APK file is named `app.apk` and placed in the same directory
   - Click "2. Upload APK" button
   - Wait for the upload to complete

5. **Verify Device**
   - Click "3. Verify" button
   - The application will verify the device configuration
   - Check the results in the activity log

6. **Complete the Process**
   - Review all logs to ensure success
   - Disconnect the device
   - Move to the next device

### Using a Hardware QR Scanner

Most USB barcode/QR scanners work as keyboard input devices. Simply:
1. Click in the "Scan QR Code" field
2. Scan the QR code with your scanner
3. The scanner will automatically "type" the serial number

## Configuration

### Custom APK Location

To use a custom APK file location, modify the `apk_path` variable in the `upload_apk` method of `main.py`:

```python
apk_path = "path/to/your/app.apk"
```

### Adding Custom Tests

To add custom test steps, modify the `run_tests` method in `main.py`. Each test follows this pattern:

```python
success, output = self.run_adb_command(
    ['adb', 'shell', 'your-command'],
    "Description of your test"
)
```

## Troubleshooting

### ADB Not Found
- Ensure Android SDK Platform Tools are installed
- Verify ADB is in your system PATH
- Restart the application after installing ADB

### Device Not Detected
- Check the USB cable connection
- Enable USB debugging on the device (if applicable)
- Try running `adb devices` in Command Prompt to verify connectivity
- Click the "Refresh" button in the application

### APK Installation Fails
- Verify the APK file exists and is not corrupted
- Ensure there's enough storage space on the device
- Check if the package is already installed (use `-r` flag to replace)

## Development

### Project Structure

```
air-caps-apk-update/
├── main.py              # Main application file
├── requirements.txt     # Python dependencies
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Extending the Application

The application is built with Python's tkinter library and uses ADB (Android Debug Bridge) for device communication. Key components:

- **AirCapsReworkTool class**: Main application logic
- **UI Components**: Tkinter-based graphical interface
- **Threading**: Background operations for non-blocking UI
- **ADB Integration**: Subprocess calls to ADB commands

## License

[Add your license information here]

## Support

For issues or questions, please contact the development team or open an issue on GitHub.