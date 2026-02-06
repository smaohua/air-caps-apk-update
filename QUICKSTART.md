# Quick Start Guide

## Air-Caps Smart Glasses Rework Tool

### First Time Setup (5 minutes)

#### Step 1: Install Python
1. Download Python 3.7+ from https://www.python.org/downloads/
2. Run installer and **CHECK** "Add Python to PATH"
3. Complete installation

#### Step 2: Install ADB (Android Debug Bridge)
1. Download from https://developer.android.com/studio/releases/platform-tools
2. Extract to `C:\platform-tools`
3. Add to system PATH:
   - Right-click "This PC" → Properties → Advanced System Settings
   - Click "Environment Variables"
   - Under "System variables", find "Path", click Edit
   - Click New, add `C:\platform-tools`
   - Click OK on all dialogs
4. Restart Command Prompt

#### Step 3: Verify Installation
Open Command Prompt and test:
```cmd
python --version
adb version
```

Both should display version information.

### Running the Tool

#### Option 1: Using Batch File (Easiest)
Double-click `start.bat`

#### Option 2: Using Command Prompt
```cmd
cd path\to\air-caps-apk-update
python main.py
```

### Daily Workflow

1. **Start Application**
   - Double-click `start.bat` or run `python main.py`

2. **Connect Device**
   - Connect smart glasses via USB cable
   - Wait for green "Device Connected" status

3. **For Each Device:**
   - Scan QR code (serial number appears in field)
   - Click "1. Run Tests" → Wait for completion
   - Click "2. Upload APK" → Wait for completion
   - Click "3. Verify" → Wait for completion
   - Check logs for any errors
   - Disconnect and move to next device

### Tips for Operators

- Keep QR scanner focused on the serial number field
- Wait for each operation to complete before starting the next
- Check the activity log for any red ERROR messages
- If a device fails, note the serial number and set it aside
- Refresh device connection if it's not detected

### Troubleshooting

**Device Not Detected?**
- Check USB cable
- Click "Refresh" button
- Try different USB port
- Run `adb devices` in Command Prompt

**QR Scanner Not Working?**
- Ensure cursor is in the serial number field
- Check scanner USB connection
- Try scanning again

**APK Upload Fails?**
- Ensure `app.apk` file exists in the program folder
- Check device storage space
- Try disconnecting and reconnecting device

### Support

For technical issues, contact IT support or check the README.md file for detailed documentation.
