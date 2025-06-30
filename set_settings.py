import os
import shutil

##########################################
# Set parameters in the esme file
##########################################
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

