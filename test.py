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
input_dicom = gsps.add_graphic_layer(input_dicom, "LAYER1", "for annotation", 1)
input_dicom = gsps.add_displayed_area_selection(input_dicom, input_dicom.Columns, input_dicom.Rows)
text = gsps.get_text_annotation(annotation_text, text_bounding_box, anchor_point)
circle = gsps.get_circle(cir_rad, cir_pos_x, cir_pos_y)
circle2 = gsps.get_circle(cir_rad + 20, cir_pos_x, cir_pos_y)
circle3 = gsps.get_circle(cir_rad, cir_pos_x + 200, cir_pos_y + 100)
input_dicom = gsps.add_graphic_annotations(input_dicom, "LAYER1", [circle, circle2, circle3], [text])
print("OK: add annotation")

# write output
input_dicom.save_as("./images/sample_annotation.dcm")
