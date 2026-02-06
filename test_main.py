#!/usr/bin/env python3
"""
Test script for air-caps-apk-update application
Validates the application structure and basic functionality
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
import tkinter as tk

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the main application
import main


class TestAirCapsReworkTool(unittest.TestCase):
    """Test cases for Air-Caps Rework Tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.root = tk.Tk()
        self.root.withdraw()  # Hide window during tests
    
    def tearDown(self):
        """Clean up after tests"""
        try:
            self.root.destroy()
        except Exception:
            pass
    
    def test_application_initialization(self):
        """Test that the application initializes correctly"""
        app = main.AirCapsReworkTool(self.root)
        
        # Check that key components are initialized
        self.assertIsNotNone(app.serial_number)
        self.assertIsNotNone(app.device_connected)
        self.assertIsNotNone(app.current_operation)
        self.assertIsNotNone(app.log_queue)
    
    def test_serial_number_handling(self):
        """Test serial number input and handling"""
        app = main.AirCapsReworkTool(self.root)
        
        # Set a serial number
        test_serial = "SN-12345-TEST"
        app.serial_number.set(test_serial)
        
        # Verify it was set
        self.assertEqual(app.serial_number.get(), test_serial)
        
        # Clear serial number
        app.clear_serial()
        self.assertEqual(app.serial_number.get(), "")
    
    def test_logging_functionality(self):
        """Test logging functionality"""
        app = main.AirCapsReworkTool(self.root)
        
        # Log a message
        test_message = "Test log message"
        app.log(test_message, "INFO")
        
        # Process the queue
        app.root.update()
        
        # Check that log queue received the message
        self.assertFalse(app.log_queue.empty())
    
    def test_button_state_updates(self):
        """Test that buttons are enabled/disabled correctly"""
        app = main.AirCapsReworkTool(self.root)
        
        # Initially, buttons should be disabled (no device, no serial)
        app.update_button_states()
        self.assertEqual(app.test_btn.cget('state'), 'disabled')
        
        # Set serial and device connected
        app.serial_number.set("SN-TEST-123")
        app.device_connected.set(True)
        app.update_button_states()
        
        # Buttons should now be enabled
        self.assertEqual(app.test_btn.cget('state'), 'normal')
        self.assertEqual(app.upload_btn.cget('state'), 'normal')
        self.assertEqual(app.verify_btn.cget('state'), 'normal')
    
    @patch('subprocess.run')
    def test_adb_command_execution(self, mock_run):
        """Test ADB command execution"""
        app = main.AirCapsReworkTool(self.root)
        
        # Mock successful ADB command
        mock_run.return_value = Mock(
            returncode=0,
            stdout="device",
            stderr=""
        )
        
        success, output = app.run_adb_command(
            ['adb', 'get-state'],
            "Test ADB command"
        )
        
        self.assertTrue(success)
        self.assertEqual(output, "device")
        mock_run.assert_called_once()
    
    @patch('subprocess.run')
    def test_adb_availability_check(self, mock_run):
        """Test ADB availability check"""
        app = main.AirCapsReworkTool(self.root)
        
        # Mock ADB version command
        mock_run.return_value = Mock(
            returncode=0,
            stdout="Android Debug Bridge version 1.0.41",
            stderr=""
        )
        
        result = app.check_adb()
        self.assertTrue(result)
    
    def test_ui_components_exist(self):
        """Test that all required UI components are created"""
        app = main.AirCapsReworkTool(self.root)
        
        # Check key UI elements exist
        self.assertIsNotNone(app.sn_entry)
        self.assertIsNotNone(app.test_btn)
        self.assertIsNotNone(app.upload_btn)
        self.assertIsNotNone(app.verify_btn)
        self.assertIsNotNone(app.log_text)
        self.assertIsNotNone(app.progress)
        self.assertIsNotNone(app.device_status_label)


class TestApplicationStructure(unittest.TestCase):
    """Test the overall application structure"""
    
    def test_main_function_exists(self):
        """Test that main function exists"""
        self.assertTrue(hasattr(main, 'main'))
        self.assertTrue(callable(main.main))
    
    def test_aircaps_class_exists(self):
        """Test that AirCapsReworkTool class exists"""
        self.assertTrue(hasattr(main, 'AirCapsReworkTool'))


def run_tests():
    """Run all tests"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestAirCapsReworkTool))
    suite.addTests(loader.loadTestsFromTestCase(TestApplicationStructure))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())
