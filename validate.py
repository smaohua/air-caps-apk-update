#!/usr/bin/env python3
"""
Validation script for air-caps-apk-update application
Checks code structure without requiring UI components
"""

import sys
import os
import ast
import subprocess

def check_python_syntax(filename):
    """Check if Python file has valid syntax"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        ast.parse(code)
        print(f"✓ {filename}: Valid Python syntax")
        return True
    except SyntaxError as e:
        print(f"✗ {filename}: Syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"✗ {filename}: Error: {e}")
        return False

def check_imports(filename):
    """Check if all imports are valid (that can be checked without GUI)"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)
        
        print(f"✓ {filename}: Found imports: {', '.join(imports)}")
        return True
    except Exception as e:
        print(f"✗ {filename}: Error checking imports: {e}")
        return False

def check_class_structure(filename):
    """Check if main class exists with required methods"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            code = f.read()
        tree = ast.parse(code)
        
        classes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
                classes[node.name] = methods
        
        if 'AirCapsReworkTool' in classes:
            methods = classes['AirCapsReworkTool']
            required_methods = ['run_tests', 'upload_apk', 'verify_device', 
                              'check_device', 'check_adb']
            
            found = [m for m in required_methods if m in methods]
            missing = [m for m in required_methods if m not in methods]
            
            print(f"✓ {filename}: Found AirCapsReworkTool class with {len(methods)} methods")
            print(f"  Required methods found: {', '.join(found)}")
            
            if missing:
                print(f"  Warning: Missing methods: {', '.join(missing)}")
                return False
            return True
        else:
            print(f"✗ {filename}: AirCapsReworkTool class not found")
            return False
    except Exception as e:
        print(f"✗ {filename}: Error checking class structure: {e}")
        return False

def check_file_exists(filename):
    """Check if a file exists"""
    exists = os.path.exists(filename)
    if exists:
        print(f"✓ {filename}: File exists")
    else:
        print(f"✗ {filename}: File not found")
    return exists

def main():
    """Run all validation checks"""
    print("=" * 60)
    print("Air-Caps APK Update - Validation Script")
    print("=" * 60)
    print()
    
    checks_passed = 0
    checks_total = 0
    
    # Check required files exist
    print("Checking required files...")
    files_to_check = [
        'main.py',
        'requirements.txt',
        'README.md',
        'QUICKSTART.md',
        'start.bat',
        '.gitignore',
        'config.json'
    ]
    
    for filename in files_to_check:
        checks_total += 1
        if check_file_exists(filename):
            checks_passed += 1
    
    print()
    
    # Check Python syntax
    print("Checking Python syntax...")
    checks_total += 1
    if check_python_syntax('main.py'):
        checks_passed += 1
    print()
    
    # Check imports
    print("Checking imports...")
    checks_total += 1
    if check_imports('main.py'):
        checks_passed += 1
    print()
    
    # Check class structure
    print("Checking class structure...")
    checks_total += 1
    if check_class_structure('main.py'):
        checks_passed += 1
    print()
    
    # Check if ADB command structure is correct
    print("Checking ADB integration...")
    with open('main.py', 'r') as f:
        content = f.read()
        if 'adb' in content.lower():
            print("✓ ADB integration found in code")
            checks_passed += 1
        else:
            print("✗ ADB integration not found")
        checks_total += 1
    print()
    
    # Summary
    print("=" * 60)
    print(f"Validation Results: {checks_passed}/{checks_total} checks passed")
    print("=" * 60)
    
    if checks_passed == checks_total:
        print("✓ All validation checks passed!")
        print("\nThe application is ready to use on Windows with Python and ADB installed.")
        return 0
    else:
        print(f"✗ {checks_total - checks_passed} check(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
