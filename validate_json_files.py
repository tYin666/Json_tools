#!/usr/bin/env python3
"""
JSON File Validator for ISSP Project
=====================================

This script validates the JSON syntax of ESME and dataset files 
after they have been modified by set_settings.py.

Usage:
    python validate_json_files.py <project_folder>
    
Example:
    python validate_json_files.py /path/to/project
"""

import os
import sys
import json

def validate_json_file(file_path, file_type="JSON"):
    """
    Validate if a JSON file is properly formatted.
    
    Args:
        file_path (str): Path to the JSON file
        file_type (str): Type description for reporting
        
    Returns:
        bool: True if valid, False if invalid
    """
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        print(f"✅ {file_type} file is valid: {file_path}")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ {file_type} file has JSON syntax error: {file_path}")
        print(f"   Error: {str(e)}")
        return False
    except FileNotFoundError:
        print(f"❌ {file_type} file not found: {file_path}")
        return False
    except Exception as e:
        print(f"❌ {file_type} file validation failed: {file_path}")
        print(f"   Error: {str(e)}")
        return False

def find_json_files(prj_folder):
    """
    Find ESME and dataset JSON files in the project folder.
    
    Args:
        prj_folder (str): Project folder path
        
    Returns:
        tuple: (esme_path, dataset_path)
    """
    esme_path = None
    dataset_path = None
    
    for root, dirs, files in os.walk(prj_folder):
        if "esme_manifest_issp_roudi.json" in files and esme_path is None:
            esme_path = os.path.join(root, "esme_manifest_issp_roudi.json")
        if "issp_dataset.json" in files and dataset_path is None:
            dataset_path = os.path.join(root, "issp_dataset.json")
        if esme_path and dataset_path:
            break
    
    return esme_path, dataset_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_json_files.py <project_folder>")
        print("Example: python validate_json_files.py /path/to/project")
        sys.exit(1)
    
    prj_folder = sys.argv[1]
    
    if not os.path.exists(prj_folder):
        print(f"❌ Project folder not found: {prj_folder}")
        sys.exit(1)
    
    print("="*70)
    print("JSON FILE VALIDATION FOR ISSP PROJECT")
    print("="*70)
    print(f"Project folder: {prj_folder}")
    print()
    
    # Find JSON files
    esme_path, dataset_path = find_json_files(prj_folder)
    
    validation_results = []
    
    # Validate ESME JSON file
    if esme_path:
        print(f"Found ESME file: {esme_path}")
        is_valid = validate_json_file(esme_path, "ESME JSON")
        validation_results.append(("ESME", esme_path, is_valid))
    else:
        print("ℹ️  ESME file (esme_manifest_issp_roudi.json) not found")
    
    # Validate Dataset JSON file  
    if dataset_path:
        print(f"Found Dataset file: {dataset_path}")
        is_valid = validate_json_file(dataset_path, "Dataset JSON")
        validation_results.append(("Dataset", dataset_path, is_valid))
    else:
        print("ℹ️  Dataset file (issp_dataset.json) not found")
    
    # Summary
    print("\n" + "-"*70)
    print("VALIDATION SUMMARY:")
    print("-"*70)
    
    if validation_results:
        all_valid = True
        for file_type, path, is_valid in validation_results:
            status = "✅ VALID" if is_valid else "❌ INVALID"
            print(f"{file_type:10} {status:10} {os.path.basename(path)}")
            if not is_valid:
                all_valid = False
        
        print()
        if all_valid:
            print(f"🎉 SUCCESS: All {len(validation_results)} JSON file(s) are valid!")
            print("   Files are ready for use in the ISSP system.")
        else:
            invalid_count = sum(1 for _, _, valid in validation_results if not valid)
            print(f"⚠️  WARNING: {invalid_count} file(s) have validation errors!")
            print("   Please check the error messages above and fix any JSON syntax issues.")
            sys.exit(1)
    else:
        print("ℹ️  No JSON files found for validation.")
        print("   Make sure the project folder contains:")
        print("   - esme_manifest_issp_roudi.json")
        print("   - issp_dataset.json")
    
    print("="*70)

if __name__ == "__main__":
    main()
