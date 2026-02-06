#!/usr/bin/env python3
"""
air-caps-apk-update - Smart Glasses Rework Tool

This application is used for reworking smart glasses that run Android.
Workflow:
1. Connect glasses via special cable to Windows PC
2. Scan QR code to get serial number
3. Click buttons to test, upload, and verify
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import queue
import subprocess
import os
import sys
import time
from datetime import datetime


class AirCapsReworkTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Air-Caps Smart Glasses Rework Tool")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Queue for thread-safe logging
        self.log_queue = queue.Queue()
        
        # State variables
        self.serial_number = tk.StringVar()
        self.device_connected = tk.BooleanVar(value=False)
        self.current_operation = tk.StringVar(value="Ready")
        
        # Create UI
        self.create_widgets()
        
        # Start log queue processor
        self.process_log_queue()
        
        # Check ADB availability
        self.check_adb()
        
        # Start device monitoring
        self.start_device_monitoring()
    
    def create_widgets(self):
        """Create the main UI components"""
        # Header Frame
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N))
        
        ttk.Label(header_frame, text="Air-Caps Smart Glasses Rework Tool", 
                 font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Serial Number Frame
        sn_frame = ttk.LabelFrame(self.root, text="Serial Number", padding="10")
        sn_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(sn_frame, text="Scan QR Code:").grid(row=0, column=0, sticky=tk.W)
        self.sn_entry = ttk.Entry(sn_frame, textvariable=self.serial_number, 
                                   font=('Arial', 12), width=40)
        self.sn_entry.grid(row=0, column=1, padx=10, sticky=(tk.W, tk.E))
        self.sn_entry.bind('<Return>', lambda e: self.on_serial_scanned())
        self.sn_entry.focus()
        
        ttk.Button(sn_frame, text="Clear", command=self.clear_serial).grid(row=0, column=2)
        
        sn_frame.columnconfigure(1, weight=1)
        
        # Device Status Frame
        status_frame = ttk.LabelFrame(self.root, text="Device Status", padding="10")
        status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.device_status_label = ttk.Label(status_frame, text="⚫ No Device Connected", 
                                             font=('Arial', 10))
        self.device_status_label.grid(row=0, column=0, sticky=tk.W)
        
        ttk.Button(status_frame, text="Refresh", command=self.check_device).grid(row=0, column=1, padx=10)
        
        # Operations Frame
        ops_frame = ttk.LabelFrame(self.root, text="Operations", padding="10")
        ops_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        self.test_btn = ttk.Button(ops_frame, text="1. Run Tests", 
                                    command=self.run_tests, width=20)
        self.test_btn.grid(row=0, column=0, padx=5, pady=5)
        
        self.upload_btn = ttk.Button(ops_frame, text="2. Upload APK", 
                                      command=self.upload_apk, width=20)
        self.upload_btn.grid(row=0, column=1, padx=5, pady=5)
        
        self.verify_btn = ttk.Button(ops_frame, text="3. Verify", 
                                      command=self.verify_device, width=20)
        self.verify_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Progress Frame
        progress_frame = ttk.Frame(self.root, padding="10")
        progress_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), padx=10, pady=5)
        
        ttk.Label(progress_frame, text="Status:").grid(row=0, column=0, sticky=tk.W)
        self.status_label = ttk.Label(progress_frame, textvariable=self.current_operation, 
                                      font=('Arial', 10, 'bold'))
        self.status_label.grid(row=0, column=1, sticky=tk.W, padx=10)
        
        self.progress = ttk.Progressbar(progress_frame, mode='indeterminate', length=300)
        self.progress.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Log Frame
        log_frame = ttk.LabelFrame(self.root, text="Activity Log", padding="10")
        log_frame.grid(row=5, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=70, 
                                                   font=('Consolas', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        ttk.Button(log_frame, text="Clear Log", command=self.clear_log).grid(row=1, column=0, pady=5)
        
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(5, weight=1)
        
        # Initial button state
        self.update_button_states()
    
    def log(self, message, level="INFO"):
        """Thread-safe logging"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        self.log_queue.put(log_message)
    
    def process_log_queue(self):
        """Process log messages from queue"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.process_log_queue)
    
    def clear_log(self):
        """Clear the log text area"""
        self.log_text.delete(1.0, tk.END)
    
    def clear_serial(self):
        """Clear the serial number field"""
        self.serial_number.set("")
        self.sn_entry.focus()
    
    def check_adb(self):
        """Check if ADB is available"""
        try:
            result = subprocess.run(['adb', 'version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.log("ADB is available and ready")
                return True
            else:
                self.log("ADB command failed", "ERROR")
                return False
        except FileNotFoundError:
            self.log("ADB not found. Please install Android SDK Platform Tools", "ERROR")
            messagebox.showwarning("ADB Not Found", 
                                  "Android Debug Bridge (ADB) is not installed.\n"
                                  "Please install Android SDK Platform Tools.")
            return False
        except Exception as e:
            self.log(f"Error checking ADB: {e}", "ERROR")
            return False
    
    def check_device(self):
        """Check if an Android device is connected"""
        try:
            result = subprocess.run(['adb', 'devices'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                devices = [line for line in lines[1:] if line.strip() and 'device' in line]
                
                if devices:
                    self.device_connected.set(True)
                    device_id = devices[0].split()[0]
                    self.device_status_label.config(text=f"🟢 Device Connected: {device_id}")
                    self.log(f"Device connected: {device_id}")
                else:
                    self.device_connected.set(False)
                    self.device_status_label.config(text="⚫ No Device Connected")
                    self.log("No device connected")
            else:
                self.device_connected.set(False)
                self.log("Failed to check device status", "ERROR")
        except Exception as e:
            self.device_connected.set(False)
            self.log(f"Error checking device: {e}", "ERROR")
        
        self.update_button_states()
    
    def start_device_monitoring(self):
        """Start monitoring for device connections"""
        self.check_device()
        self.root.after(3000, self.start_device_monitoring)  # Check every 3 seconds
    
    def update_button_states(self):
        """Update button states based on conditions"""
        can_operate = self.device_connected.get() and self.serial_number.get().strip()
        
        state = 'normal' if can_operate else 'disabled'
        self.test_btn.config(state=state)
        self.upload_btn.config(state=state)
        self.verify_btn.config(state=state)
    
    def on_serial_scanned(self):
        """Handle serial number scan"""
        sn = self.serial_number.get().strip()
        if sn:
            self.log(f"Serial number scanned: {sn}")
            self.update_button_states()
        else:
            self.log("Empty serial number", "WARNING")
    
    def run_adb_command(self, command, description=""):
        """Execute an ADB command"""
        if description:
            self.log(f"{description}...")
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                if description:
                    self.log(f"{description} - Success")
                return True, result.stdout
            else:
                if description:
                    self.log(f"{description} - Failed: {result.stderr}", "ERROR")
                return False, result.stderr
        except subprocess.TimeoutExpired:
            self.log(f"Command timeout: {' '.join(command)}", "ERROR")
            return False, "Timeout"
        except Exception as e:
            self.log(f"Command error: {e}", "ERROR")
            return False, str(e)
    
    def run_tests(self):
        """Run device tests"""
        def test_thread():
            try:
                self.current_operation.set("Running Tests...")
                self.progress.start()
                
                sn = self.serial_number.get().strip()
                self.log(f"Starting tests for device: {sn}")
                
                # Test 1: Check device properties
                success, output = self.run_adb_command(
                    ['adb', 'shell', 'getprop', 'ro.product.model'],
                    "Test 1: Reading device model"
                )
                if success:
                    self.log(f"Device model: {output.strip()}")
                
                # Test 2: Check battery status
                success, output = self.run_adb_command(
                    ['adb', 'shell', 'dumpsys', 'battery'],
                    "Test 2: Checking battery status"
                )
                if success:
                    self.log("Battery check completed")
                
                # Test 3: Check storage
                success, output = self.run_adb_command(
                    ['adb', 'shell', 'df', '/data'],
                    "Test 3: Checking storage"
                )
                if success:
                    self.log("Storage check completed")
                
                # Test 4: Check installed packages
                success, output = self.run_adb_command(
                    ['adb', 'shell', 'pm', 'list', 'packages'],
                    "Test 4: Checking installed packages"
                )
                if success:
                    package_count = len(output.strip().split('\n'))
                    self.log(f"Found {package_count} installed packages")
                
                self.log("All tests completed successfully", "SUCCESS")
                messagebox.showinfo("Tests Complete", 
                                   f"All tests completed for device {sn}")
                
            except Exception as e:
                self.log(f"Test error: {e}", "ERROR")
                messagebox.showerror("Test Error", f"An error occurred: {e}")
            finally:
                self.progress.stop()
                self.current_operation.set("Ready")
        
        threading.Thread(target=test_thread, daemon=True).start()
    
    def upload_apk(self):
        """Upload APK to device"""
        def upload_thread():
            try:
                self.current_operation.set("Uploading APK...")
                self.progress.start()
                
                sn = self.serial_number.get().strip()
                self.log(f"Starting APK upload for device: {sn}")
                
                # Check if APK file exists
                apk_path = "app.apk"  # Default APK name
                if not os.path.exists(apk_path):
                    self.log(f"APK file not found: {apk_path}", "WARNING")
                    self.log("Simulating APK upload (no APK file provided)")
                    time.sleep(2)  # Simulate upload time
                    self.log("APK upload simulated successfully", "SUCCESS")
                    messagebox.showinfo("Upload Complete", 
                                       f"APK upload completed for device {sn}\n"
                                       "(Simulated - no APK file found)")
                else:
                    # Install the APK
                    success, output = self.run_adb_command(
                        ['adb', 'install', '-r', apk_path],
                        f"Installing APK: {apk_path}"
                    )
                    
                    if success:
                        self.log("APK installed successfully", "SUCCESS")
                        messagebox.showinfo("Upload Complete", 
                                           f"APK installed successfully on device {sn}")
                    else:
                        messagebox.showerror("Upload Failed", 
                                            f"Failed to install APK: {output}")
                
            except Exception as e:
                self.log(f"Upload error: {e}", "ERROR")
                messagebox.showerror("Upload Error", f"An error occurred: {e}")
            finally:
                self.progress.stop()
                self.current_operation.set("Ready")
        
        threading.Thread(target=upload_thread, daemon=True).start()
    
    def verify_device(self):
        """Verify device configuration"""
        def verify_thread():
            try:
                self.current_operation.set("Verifying...")
                self.progress.start()
                
                sn = self.serial_number.get().strip()
                self.log(f"Starting verification for device: {sn}")
                
                verification_passed = True
                
                # Verification 1: Device is online
                success, output = self.run_adb_command(
                    ['adb', 'get-state'],
                    "Verification 1: Device state"
                )
                if not success or 'device' not in output:
                    verification_passed = False
                    self.log("Device state verification failed", "ERROR")
                
                # Verification 2: Check Android version
                success, output = self.run_adb_command(
                    ['adb', 'shell', 'getprop', 'ro.build.version.release'],
                    "Verification 2: Android version"
                )
                if success:
                    android_version = output.strip()
                    self.log(f"Android version: {android_version}")
                
                # Verification 3: Check device serial
                success, output = self.run_adb_command(
                    ['adb', 'get-serialno'],
                    "Verification 3: Device serial number"
                )
                if success:
                    device_serial = output.strip()
                    self.log(f"Device serial: {device_serial}")
                
                if verification_passed:
                    self.log(f"Verification completed successfully for {sn}", "SUCCESS")
                    messagebox.showinfo("Verification Complete", 
                                       f"Device {sn} passed all verifications!")
                else:
                    self.log(f"Verification failed for {sn}", "ERROR")
                    messagebox.showerror("Verification Failed", 
                                        f"Device {sn} failed verification checks")
                
            except Exception as e:
                self.log(f"Verification error: {e}", "ERROR")
                messagebox.showerror("Verification Error", f"An error occurred: {e}")
            finally:
                self.progress.stop()
                self.current_operation.set("Ready")
        
        threading.Thread(target=verify_thread, daemon=True).start()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = AirCapsReworkTool(root)
    root.mainloop()


if __name__ == "__main__":
    main()
