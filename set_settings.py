import os
import shutil
<<<<<<< HEAD
import sys
import json
=======
>>>>>>> c422ef4f390e7d48547d9b842d9fd132a73e8962

##########################################
# Set parameters in the esme file
##########################################
<<<<<<< HEAD

if len(sys.argv) < 2:
    print("Usage: python set_settings.py <prj_folder_path>")
    sys.exit(1)

prj_folder = sys.argv[1]

found_esme = False
found_dataset = False
dataset_path = None
esme_path = None
for root, dirs, files in os.walk(prj_folder):
    if "esme_manifest_issp_roudi.json" in files and not found_esme:
        esme_path = os.path.join(root, "esme_manifest_issp_roudi.json")
        print(f"esme json found, path is {esme_path}")
        found_esme = True
    if "issp_dataset.json" in files and not found_dataset:
        dataset_path = os.path.join(root, "issp_dataset.json")
        print(f"dataset json found, path is {dataset_path}")
        found_dataset = True
    if found_esme and found_dataset:
        break
if not found_esme and not found_dataset:
    print("Neither esme_manifest_issp_roudi.json nor issp_dataset.json found in project folder.")
elif not found_esme:
    print("esme_manifest_issp_roudi.json not found in project folder.")
elif not found_dataset:
    print("issp_dataset.json not found in project folder.")



if esme_path is not None and os.path.exists(esme_path) and not os.path.exists(esme_path + ".bak"):
    shutil.copyfile(esme_path, esme_path + ".bak")
    print(f"Created backup: {esme_path}.bak")
    
if dataset_path is not None and os.path.exists(dataset_path) and not os.path.exists(dataset_path + ".bak"):
    shutil.copyfile(dataset_path, dataset_path + ".bak")
    print(f"Created backup: {dataset_path}.bak")

##########################################
# Load replacements from a JSON file
##########################################

replacements_json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "esme_replacements.json")
if not os.path.exists(replacements_json_path):
    print(f"Replacement file not found: {replacements_json_path}")
    sys.exit(1)

with open(replacements_json_path, "r") as f:
    replacements_data = json.load(f)

if "replacements" not in replacements_data:
    print("Error: 'replacements' key not found in JSON file")
    sys.exit(1)

replacements = replacements_data["replacements"]
print(f"Loaded {len(replacements)} replacement rules from {replacements_json_path}")

# replacements should be a list of {"from": ..., "to": ...}
if esme_path is None:
    print("esme_path is not set. Cannot proceed.")
    sys.exit(1)

try:
    with open(esme_path, "r") as fh:
        esme_data = fh.read()
except IOError as e:
    print(f"Error reading ESME file {esme_path}: {e}")
    sys.exit(1)

# Note: Using str.replace in a loop can cause cascading replacements if the "to" value of one replacement matches the "from" value of another.
# To avoid this, we use regular expressions to perform all replacements in a single pass.
import re

def multiple_replace(text, replacements):
    """
    Perform multiple string replacements in a single pass to avoid cascading replacements.
    
    Args:
        text (str): The input text to perform replacements on
        replacements (list): List of replacement dictionaries with 'from' and 'to' keys
        
    Returns:
        str: Text with all replacements applied
    """
    # Build a regex pattern with all "from" values escaped
    rep_dict = {rep["from"]: rep["to"] for rep in replacements}
    pattern = re.compile("|".join(re.escape(k) for k in rep_dict.keys()))
    
    def replace_func(match):
        return rep_dict[match.group(0)]
    
    return pattern.sub(replace_func, text)

print(f"Applying {len(replacements)} replacements to ESME file...")
esme_data = multiple_replace(esme_data, replacements)

print(f"Successfully applied replacements to {esme_path}")

try:
    with open(esme_path, "w") as fh:
        fh.write(esme_data)
    print(f"ESME file updated successfully: {esme_path}")
except IOError as e:
    print(f"Error writing to ESME file {esme_path}: {e}")
    sys.exit(1)



##########################################
# Set parameters in the dataset file
=======
esme_file="issp_aos_dply_oms_only/aos/yaaac_codegen/deploy/carma_0_22/issp_roudi/esme/esme_manifest_issp_roudi.json"

if os.path.exists(esme_file + ".bak"):
    shutil.copyfile(esme_file + ".bak", esme_file)
else:
    shutil.copyfile(esme_file, esme_file + ".bak")

with open(esme_file, "r") as fh:
    esme_data = fh.read()

esme_data = esme_data.replace("ISSP_AOS_PARAM_GW_VARIANT_TYPE=9", "ISSP_AOS_PARAM_GW_VARIANT_TYPE=9")
esme_data = esme_data.replace("ISSP_AOS_PARAM_GW_CAM=0", "ISSP_AOS_PARAM_GW_CAM=0")
esme_data = esme_data.replace(
    "\"MGC_BODYPOSE2D_MODEL_PATH=/home/iss/issp_oms_models/bodypose2d_model.onnx\"",
    "\"MGC_BODYPOSE2D_MODEL_PATH=/home/issp/workspace/issp_oms_models/bodypose2d_model.onnx\",\n                                    \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace/issp_oms_so\",\n\"MGC_BODYPOSE2D_PEAKS_THRESHOLD=0.125\",\n\"MGC_BODYPOSE2D_CONNECT_THRESHOLD=0.05\"")

esme_data = esme_data.replace(
    "\"MGC_BODYPOSE3D_MODEL_PATH=/home/iss/issp_oms_models/bodypose3d_model.onnx\"",
    "\"MGC_BODYPOSE3D_MODEL_PATH=/home/issp/workspace/issp_oms_models/bodypose3d_model.onnx\",\n                                    \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace//issp_oms_so\"")


esme_data = esme_data.replace(
    "\"MGC_SEATBELT_MODEL_PATH=/home/iss/issp_oms_models/seatbelt_model.onnx\"",
    "\"MGC_SEATBELT_MODEL_PATH=/home/issp/workspace/issp_oms_models/seatbelt_model.onnx\"")

esme_data = esme_data.replace(
    "\"MGC_SEATBELT_MISUSE_MODEL_PATH=/home/iss/issp_oms_models/seatbelt_misuse_model.onnx\"",
    "\"MGC_SEATBELT_MISUSE_MODEL_PATH=/home/issp/workspace/issp_oms_models/seatbelt_misuse_model.onnx\",\n                                    \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace//issp_oms_so\"")

esme_data = esme_data.replace(
    "\"MGC_CHILDSEATDET2D_MODEL_PATH=/home/iss/issp_oms_models/crs2d_model.onnx\"",
    "\"MGC_CHILDSEATDET2D_MODEL_PATH=/home/issp/workspace/issp_oms_models/crs2d_model.onnx\",\n                                    \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace//issp_oms_so\"")

esme_data = esme_data.replace(
    "\"ACTIVITY_INSTANCE_NAME=issp_aos_act_bp2hp_instance\"",
    "\"ACTIVITY_INSTANCE_NAME=issp_aos_act_bp2hp_instance\",\n                                    \"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/issp/workspace//issp_oms_so\"")




with open(esme_file, "w") as fh:
    fh.write(esme_data)


##########################################
# Set parameters in the esme file
>>>>>>> c422ef4f390e7d48547d9b842d9fd132a73e8962
##########################################
#dataset_file="dataset/issp_dataset.json"

#if os.path.exists(dataset_file + ".bak"):
#    shutil.copyfile(dataset_file + ".bak", dataset_file)
#else:
#    shutil.copyfile(dataset_file, dataset_file + ".bak")

#with open(dataset_file, "r") as fh:
#    dataset_data = fh.read()

#dataset_data = dataset_data.replace('"input_source": 0', '"input_source": 2')

#with open(dataset_file, "w") as fh:
#    fh.write(dataset_data)

