# ISSP JSON Tools Documentation

This repository contains a collection of tools for working with JSON configuration files in ISSP (Intelligent Safety System Platform) projects.

## Overview

The JSON Tools package provides utilities for:
- Modifying configuration parameters in ESME manifest files
- Validating JSON file syntax with detailed error reporting
- Automating project setup and configuration

## Files

### `set_settings.py` 🔧
Main configuration tool that applies predefined parameter replacements to ISSP project files.

### `checkJson.py` ✅ 
Advanced JSON validation utility with comprehensive error reporting and fix suggestions.

### `esme_replacements.json` 📋
Configuration file containing replacement rules for ESME manifest parameters.

### `test.sh` 🚀
Shell script for testing the configuration tools on sample projects.

---

## `set_settings.py` - Configuration Parameter Tool

### Purpose
This script automatically updates configuration parameters in ISSP project files by applying predefined replacements from a JSON configuration file. It's designed to standardize project configurations and update file paths, model locations, and environment variables.

### Usage
```bash
python set_settings.py <prj_folder_path>
```

**Arguments:**
- `prj_folder_path`: Path to the ISSP project folder containing the configuration files

### What it does

1. **File Discovery**: Recursively searches the project folder for:
   - `esme_manifest_issp_roudi.json` - ESME manifest configuration file
   - `issp_dataset.json` - Dataset configuration file

2. **Backup Creation**: Creates `.bak` backup copies of found files before modification

3. **Parameter Replacement**: Applies replacements from `esme_replacements.json` to the ESME manifest file

4. **Safe String Replacement**: Uses regex-based replacement to avoid cascading changes

### ⚠️ Critical Fixes Applied

**MAJOR BUG FIXED**: The original `multiple_replace()` function was completely broken:
- ❌ **Original Issue**: Function tried to write to a closed file handle and didn't return anything
- ✅ **Fixed**: Proper regex-based replacement function that returns the modified text
- ✅ **Added**: Comprehensive error handling for file operations
- ✅ **Added**: Progress feedback and validation

### Configuration File Format

The `esme_replacements.json` file contains structured replacement rules:

```json
{
    "version": "1.0",
    "description": "ESME manifest parameter replacements for ISSP project configuration",
    "replacements": [
        {
            "description": "Human-readable description of the change",
            "from": "original_value",
            "to": "new_value"
        }
    ]
}
```

### Example Replacements

The tool handles various types of configuration updates:

#### 1. Gateway Parameters
- **Variant Type**: `ISSP_AOS_PARAM_GW_VARIANT_TYPE=14` → `ISSP_AOS_PARAM_GW_VARIANT_TYPE=9`
- **Camera Settings**: Gateway camera parameter configurations

#### 2. Model Path Updates
- **Path Migration**: `/home/iss/` → `/home/issp/workspace/`
- **Models Affected**:
  - `bodypose2d_model.onnx`
  - `bodypose3d_model.onnx` 
  - `seatbelt_model.onnx`
  - `seatbelt_misuse_model.onnx`
  - `crs2d_model.onnx`

#### 3. Environment Variables
- **Library Paths**: Adds `LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace/issp_oms_so`
- **Threshold Parameters**: 
  - `MGC_BODYPOSE2D_PEAKS_THRESHOLD=0.125`
  - `MGC_BODYPOSE2D_CONNECT_THRESHOLD=0.05`

### Error Handling & Safety Features

#### Input Validation
- ✅ Command line argument validation
- ✅ File existence checks
- ✅ JSON structure validation
- ✅ Path validation

#### Backup & Recovery
- ✅ **Automatic Backups**: Creates `.bak` files before modification
- ✅ **Idempotent**: Safe to run multiple times (won't overwrite existing backups)
- ✅ **Rollback Support**: Original files preserved for recovery

#### Robust File Operations
- ✅ **Exception Handling**: Proper try/catch for all file operations
- ✅ **Detailed Error Messages**: Clear feedback on what went wrong
- ✅ **Graceful Exits**: Clean shutdown on errors

#### Safe Replacements
- ✅ **Atomic Operations**: All replacements applied in single pass
- ✅ **No Cascading**: Regex escaping prevents unintended replacements
- ✅ **Progress Feedback**: Reports number of replacements applied

### Dependencies

- Python 3.x
- Standard library modules: `os`, `shutil`, `sys`, `json`, `re`

### Example Output

```
esme json found, path is /path/to/project/esme_manifest_issp_roudi.json
dataset json found, path is /path/to/project/issp_dataset.json
Created backup: /path/to/project/esme_manifest_issp_roudi.json.bak
Loaded 8 replacement rules from /path/to/tools/esme_replacements.json
Applying 8 replacements to ESME file...
Successfully applied replacements to /path/to/project/esme_manifest_issp_roudi.json
ESME file updated successfully: /path/to/project/esme_manifest_issp_roudi.json
```

---

## `checkJson.py` - JSON Validation Tool

### Purpose
Advanced JSON validation utility that provides:
- Comprehensive syntax error detection
- Line-by-line error analysis  
- Detailed error reporting with context
- Suggested fixes for common issues
- Fixed version preview

### Usage
```bash
python checkJson.py <json_file>
```

### Features
- ✅ **Multi-Error Detection**: Finds all JSON syntax errors, not just the first one
- ✅ **Context Display**: Shows problematic lines with line numbers
- ✅ **Smart Suggestions**: Provides actionable fix recommendations
- ✅ **Fix Preview**: Shows what the corrected JSON would look like
- ✅ **Validation**: Tests if suggested fixes result in valid JSON

---

## `test.sh` - Test Script

### Purpose
Demonstrates proper usage of the configuration tools and provides a template for automation.

### ⚠️ Improvements Applied

**Enhanced Error Handling**:
- ✅ **Path Validation**: Checks if directories exist before proceeding
- ✅ **File Existence**: Verifies required scripts are present
- ✅ **Exit Code Handling**: Properly handles and reports script failures
- ✅ **User Feedback**: Clear progress messages and error reporting

### Usage
```bash
./test.sh
```

### Configuration
Edit these variables in the script:
```bash
PRJ_Folder="/path/to/your/project"
JSON_Tools_Folder="/path/to/json/tools"
if_setsettings=true  # Set to false to skip configuration
```

---

## 🔍 Issues Found & Fixed

### Critical Issues Resolved

#### 1. **BROKEN FUNCTION** in `set_settings.py`
- **Problem**: `multiple_replace()` function was completely non-functional
- **Impact**: Script would fail silently or crash
- **Fix**: Complete rewrite with proper regex handling and return values

#### 2. **Missing Error Handling**
- **Problem**: No exception handling for file operations
- **Impact**: Cryptic errors, potential data loss
- **Fix**: Comprehensive try/catch blocks with meaningful error messages

#### 3. **JSON Structure Issues**
- **Problem**: Code assumed different JSON structure than actual file
- **Impact**: Script would fail to load replacements
- **Fix**: Updated to handle actual JSON structure with proper validation

#### 4. **Shell Script Robustness**
- **Problem**: No validation of paths or error handling
- **Impact**: Silent failures, unclear error states
- **Fix**: Added comprehensive validation and error reporting

### Path Inconsistencies Fixed
- **Issue**: Double slashes in some library paths (`//issp_oms_so`)
- **Status**: ⚠️ Present in JSON file - consider standardizing

### Recommendations

#### 1. **JSON File Cleanup**
Consider standardizing the library paths in `esme_replacements.json`:
```bash
# Current (inconsistent):
/home/issp/workspace//issp_oms_so

# Suggested (consistent):
/home/issp/workspace/issp_oms_so
```

#### 2. **Add Validation Mode**
Consider adding a `--dry-run` option to preview changes without applying them.

#### 3. **Logging Enhancement**
Consider adding optional detailed logging for troubleshooting.

---

## Integration & Best Practices

### Automated Workflows
This tool is designed for integration into:
- **Build Scripts**: Automated project configuration
- **CI/CD Pipelines**: Consistent environment setup
- **Development Workflows**: Quick project standardization

### Best Practices
1. **Always backup**: The tool creates backups automatically
2. **Test first**: Use `test.sh` to validate on sample projects
3. **Validate JSON**: Use `checkJson.py` to verify configuration files
4. **Version control**: Keep `esme_replacements.json` under version control
5. **Path consistency**: Use absolute paths in configuration files

### Security Considerations
- Scripts validate input paths to prevent directory traversal
- Backup files prevent accidental data loss
- Read-only validation mode available via `checkJson.py`
