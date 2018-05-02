import gsps
import pydicom as dicom
import os
from pydicom.dataset import Dataset, FileDataset
from shutil import copyfile



# test parameter
annotation_text = 'TEST'
cir_rad, cir_pos_x, cir_pos_y = 10, 100, 100


# load the input image
input_dicom = dicom.read_file("./images/sample.dcm")
print("OK: Read dicom file")

# generate series uid
series_instance_uid = dicom.uid.generate_uid()
print("OK: Generate series uid")

# create the bare output dicom
file_meta = gsps.get_gsps_file_metadata()
ds_out = FileDataset("sample.pre", {}, file_meta=file_meta, preamble=b"\0" * 128)
print("OK: Create bare output")

# set the content description and general study fields
gsps.set_content_desription(ds_out, "Presentation State for image")
gsps.set_gsps_general_study_info(ds_out, file_meta, series_instance_uid)
print("OK: Write content description and general study fields")

# copy patient, study, series data from input image
gsps.copy_details_from_input_dicom(ds_out, input_dicom)
gsps.set_referenced_image_info(ds_out, input_dicom.SeriesInstanceUID, input_dicom.SOPClassUID,
                               input_dicom.SOPInstanceUID)
print("OK: Copy patient, study, series data from input image")

# calculate coordinates for annotation and anchor point
input_rows = input_dicom.Rows
input_columns = input_dicom.Columns
anchor_point = [input_columns / 2, input_rows / 2]

top_left = [input_columns / 10, input_rows / 5]
bottom_right = [input_columns / 5, input_rows / 5 + 16]
anchor_point = {"AnchorPointAnnotationUnits": "PIXEL", "AnchorPoint": anchor_point, "AnchorPointVisibility": "Y"}
text_bounding_box = {"BoundingBoxAnnotationUnits": "PIXEL", "BoundingBoxTopLeftHandCorner": top_left,
                     "BoundingBoxBottomRightHandCorner": bottom_right}

# add the annotation
gsps.add_graphic_layer(ds_out, "LAYER1", "for annotation", 1)
gsps.add_displayed_area_selection(ds_out, input_dicom.Columns, input_dicom.Rows)
text = gsps.get_text_annotation(annotation_text, text_bounding_box, anchor_point)
circle = gsps.get_circle(cir_rad, cir_pos_x, cir_pos_y)
circle2 = gsps.get_circle(cir_rad + 20, cir_pos_x, cir_pos_y)
circle3 = gsps.get_circle(cir_rad, cir_pos_x + 200, cir_pos_y + 100)
gsps.add_graphic_annotations(ds_out, "LAYER1", [circle, circle2, circle3], [text])
print("OK: add annotation")

# write output
ds_out.save_as("./images/sample.pre")
