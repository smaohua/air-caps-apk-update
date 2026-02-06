# Deployment Checklist

## Air-Caps Smart Glasses Rework Tool - Deployment Guide

This checklist helps ensure successful deployment of the rework tool in a production environment.

---

## Pre-Deployment Preparation

### 1. Hardware Requirements ✓
- [ ] Windows PC (Windows 7, 8, 10, or 11)
- [ ] Minimum 4GB RAM
- [ ] USB ports available for:
  - [ ] Smart glasses connection cable
  - [ ] QR code scanner (USB)
- [ ] Monitor (recommended: 1024x768 or higher)
- [ ] Mouse and keyboard

### 2. Software Installation ✓

#### Python Installation
- [ ] Download Python 3.7 or higher from python.org
- [ ] Run installer
- [ ] **IMPORTANT:** Check "Add Python to PATH" during installation
- [ ] Verify installation: Open Command Prompt and run `python --version`
- [ ] Expected: "Python 3.x.x" displayed

#### Android Debug Bridge (ADB) Installation
- [ ] Download Android SDK Platform Tools from:
  https://developer.android.com/studio/releases/platform-tools
- [ ] Extract to `C:\platform-tools` (or preferred location)
- [ ] Add to system PATH:
  - [ ] Right-click "This PC" → Properties
  - [ ] Advanced System Settings → Environment Variables
  - [ ] Find "Path" under System Variables → Edit
  - [ ] Add new entry: `C:\platform-tools`
  - [ ] Click OK on all dialogs
- [ ] **RESTART Command Prompt** after PATH changes
- [ ] Verify installation: Run `adb version`
- [ ] Expected: ADB version information displayed

#### Application Installation
- [ ] Clone or download repository from:
  https://github.com/smaohua/air-caps-apk-update
- [ ] Extract to desired location (e.g., `C:\air-caps-rework`)
- [ ] Navigate to application folder
- [ ] Run validation: `python validate.py`
- [ ] Expected: "All validation checks passed"

### 3. Configuration ✓
- [ ] Review `config.json` for any needed changes
- [ ] If using custom APK location, update `main.py` line ~354
- [ ] Place APK file in application directory (name: `app.apk`) OR
- [ ] Update APK path in configuration

### 4. Testing Before Production ✓
- [ ] Connect a test device
- [ ] Run demo: `python demo.py`
- [ ] Verify ADB detects device: `adb devices`
- [ ] Launch application: `python main.py` or double-click `start.bat`
- [ ] Test all operations:
  - [ ] Device detection works
  - [ ] Serial number entry works
  - [ ] Run Tests completes
  - [ ] Upload APK works (if test APK available)
  - [ ] Verify completes
  - [ ] Logs display correctly

---

## Day 1 Production Deployment

### Morning Setup (30 minutes)
- [ ] Power on workstation PC
- [ ] Connect QR scanner to USB port
- [ ] Launch application: Double-click `start.bat`
- [ ] Verify ADB status: Check for "ADB is available" in log
- [ ] Test QR scanner: Scan a test barcode/QR code
- [ ] Have backup PC ready in case of issues

### Operator Training (15-20 minutes)
- [ ] Show operator the QUICKSTART.md guide
- [ ] Walk through complete workflow with test device:
  1. [ ] Connect device
  2. [ ] Wait for green status
  3. [ ] Scan QR code
  4. [ ] Click "Run Tests"
  5. [ ] Wait for completion
  6. [ ] Click "Upload APK"
  7. [ ] Wait for completion
  8. [ ] Click "Verify"
  9. [ ] Review logs
  10. [ ] Disconnect device
- [ ] Practice handling common errors
- [ ] Show how to use "Clear" and "Refresh" buttons

### First Production Run (Monitor Closely)
- [ ] Supervisor present for first 5-10 devices
- [ ] Note any issues or operator questions
- [ ] Verify workflow timing (should be 1-2 min/device)
- [ ] Check log files for any unexpected errors
- [ ] Adjust procedures if needed

---

## Daily Operations Checklist

### Start of Shift
- [ ] Launch application (`start.bat`)
- [ ] Verify ADB is ready
- [ ] Test QR scanner with sample code
- [ ] Review yesterday's issues (if any)
- [ ] Clear previous day's logs if desired

### During Operations
- [ ] Monitor for error messages (red text in logs)
- [ ] Set aside any devices with failures
- [ ] Note serial numbers of failed devices
- [ ] Take breaks to prevent fatigue errors
- [ ] Keep workstation organized

### End of Shift
- [ ] Review completion count
- [ ] Note any devices set aside for rework
- [ ] Document any recurring issues
- [ ] Close application
- [ ] Disconnect all devices

---

## Troubleshooting Reference

### Problem: "ADB not found"
**Solution:**
1. Verify ADB installation: `adb version` in Command Prompt
2. Check PATH environment variable
3. Restart Command Prompt/Application
4. Reinstall Platform Tools if needed

### Problem: "No Device Connected"
**Solution:**
1. Check USB cable connection
2. Try different USB port
3. Click "Refresh" button
4. Run `adb devices` in Command Prompt
5. Verify device has USB debugging enabled
6. Try `adb kill-server` then `adb start-server`

### Problem: QR Scanner Not Working
**Solution:**
1. Click in serial number field first
2. Check scanner USB connection
3. Test scanner in Notepad
4. Verify scanner is in keyboard emulation mode

### Problem: APK Upload Fails
**Solution:**
1. Verify `app.apk` file exists
2. Check device storage space
3. Try uninstalling old version first
4. Check file permissions
5. Review error message in logs

### Problem: Application Won't Start
**Solution:**
1. Verify Python is installed: `python --version`
2. Check for syntax errors: `python validate.py`
3. Review error messages
4. Try running from Command Prompt to see errors
5. Check tkinter is available

---

## Maintenance Schedule

### Daily
- [ ] Clear old log entries (optional)
- [ ] Quick visual check of application

### Weekly
- [ ] Review any recurring errors
- [ ] Update device count statistics
- [ ] Check for software updates (Python, ADB)
- [ ] Backup configuration files

### Monthly
- [ ] Full system check
- [ ] Update documentation if procedures change
- [ ] Review operator feedback
- [ ] Plan any needed improvements

---

## Emergency Contacts

**IT Support:** [Add contact info]
**Supervisor:** [Add contact info]
**Developer/Maintainer:** [Add contact info]

---

## Important Files Locations

```
Application Directory:
├── start.bat          ← Double-click to start
├── main.py            ← Main application code
├── config.json        ← Configuration settings
├── app.apk            ← APK file to install (you provide)
├── README.md          ← Full documentation
├── QUICKSTART.md      ← Operator guide
└── validate.py        ← Installation validator
```

---

## Success Metrics

Track these daily:
- [ ] Devices processed: _____ / day
- [ ] Success rate: _____ %
- [ ] Failed devices: _____ (serial numbers: _______)
- [ ] Average time per device: _____ minutes
- [ ] Issues encountered: _____
- [ ] Downtime: _____ minutes

---

## Sign-Off

### Pre-Deployment Sign-Off
- [ ] IT Specialist: _________________ Date: _____
- [ ] Supervisor: _________________ Date: _____
- [ ] Operator Trained: _________________ Date: _____

### Post-Deployment Verification
- [ ] First day successful: Yes / No
- [ ] Issues resolved: Yes / No / N/A
- [ ] Ready for full production: Yes / No

### Notes:
_________________________________________________
_________________________________________________
_________________________________________________

---

**Document Version:** 1.0  
**Last Updated:** 2026-02-06  
**Repository:** smaohua/air-caps-apk-update
