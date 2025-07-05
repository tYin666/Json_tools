#!/bin/bash

# ISSP JSON Tools Test Script
# This script demonstrates how to use the set_settings.py tool

# Configuration - Update these paths as needed
#PRJ_Folder="/home/tie/workspace/AOS/prj_ref_3_4_0/issp_aos_dply_prj_ref"
PRJ_Folder="/home/tie/workspace/AOS/oms_only_v3.0.0-4_7_can_fusion/issp_aos_dply_oms_only"
JSON_Tools_Folder="/home/tie/workspace/ISSP/Json_Tools"

# Control flag - set to false to skip settings modification
if_setsettings=true

# Validate paths exist
if [ ! -d "$PRJ_Folder" ]; then
    echo "Error: Project folder not found: $PRJ_Folder"
    exit 1
fi

if [ ! -d "$JSON_Tools_Folder" ]; then
    echo "Error: JSON Tools folder not found: $JSON_Tools_Folder"
    exit 1
fi

if [ "$if_setsettings" = true ]; then
    echo "=== ISSP Configuration Tool ==="
    echo "Project folder: $PRJ_Folder"
    echo "Tools folder: $JSON_Tools_Folder"
    echo
    
    cd "$JSON_Tools_Folder" || exit 1
    echo "Setting settings for project folder: $PRJ_Folder"
    
    # Check if Python script exists
    if [ ! -f "set_settings.py" ]; then
        echo "Error: set_settings.py not found in $JSON_Tools_Folder"
        exit 1
    fi
    
    # Run the configuration tool
    python set_settings.py "$PRJ_Folder"
    exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo "Configuration completed successfully!"
        cd "$PRJ_Folder" || exit 1
        echo "Changed directory to: $(pwd)"
    else
        echo "Configuration failed with exit code: $exit_code"
        exit $exit_code
    fi
else
    echo "Skipping settings configuration for project folder: $PRJ_Folder"
fi


