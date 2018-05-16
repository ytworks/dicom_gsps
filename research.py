#! /usr/bin/env python
# coding:utf-8

import gsps
import pydicom as dicom
import os
from pydicom.dataset import Dataset, FileDataset
from pydicom.sequence import Sequence
from shutil import copyfile
from datetime import datetime

# load the input image

'''
input_dicom = dicom.read_file("./images/PSP/20180316.dcm")
print(input_dicom)
print("MR")
input_dicom = dicom.read_file("./images/PSP/S0000001/MR000109")
print(input_dicom)
'''

input_dicom = dicom.read_file("./images/sample.dcm")
print(input_dicom)
print("==============================================")


file_meta = Dataset()
ds = FileDataset("output_sample.dcm", {}, file_meta=file_meta, preamble=b"\0" * 128)
ds.SOPClassUID = "Grayscale Softcopy Presentation State Storage"
ds.SOPInstanceUID = dicom.uid.generate_uid()
ds.Modality = "PR"
ds.PatientID = input_dicom.PatientID
ds.PatientName = input_dicom.PatientName
ds.PatientSex = input_dicom.PatientSex
ds.PatientBirthDate = input_dicom.PatientBirthDate
ds.StudyDate = input_dicom.StudyDate
ds.Studyime = input_dicom.StudyTime
#ds.StudyDescription = input_dicom.StudyDescription
ds.ReferringPhysicianName = input_dicom.ReferringPhysicianName
#ds.AccessionNumber = input_dicom.AccessionNumber
rss = Dataset()
rss.SeriesInstanceUID = input_dicom.SeriesInstanceUID
img = Dataset()
img.SOPClassUID = input_dicom.SOPClassUID
img.SOPInstanceUID = input_dicom.SOPInstanceUID
rss.ReferencedImageSequence = Sequence([img])
ds.ReferencedSeriesSequence = Sequence([rss])

an = Dataset()
an.GraphicLayer = "Layer1"
an.ReferencedImageSequence = Sequence([img])
ds_cir_object = Dataset()
cir_pos_x, cir_pos_y, cir_rad = 300, 300, 90
ds_cir_object.GraphicAnnotationUnits = "PIXEL"
ds_cir_object.GraphicDimensions = 2
ds_cir_object.NumberOfGraphicPoints = 2
ds_cir_object.GraphicData = [
    cir_pos_x,  # x coordinate of middle of circle
    cir_pos_y,  # y coordinate of middle of circle
    cir_pos_x,  # x coordinate of point on circumference
    cir_pos_y + cir_rad]  # y coordinate of point on circumference
ds_cir_object.GraphicType = "CIRCLE"
ds_cir_object.GraphicFilled = "N"
an.GraphicObjectSequence = Sequence([ds_cir_object])
ds.GraphicAnnotationSequence = Sequence([an])
ds_displayed_area_selection = Dataset()
ds_displayed_area_selection.DisplayedAreaTopLeftHandCorner = [1, 1]
ds_displayed_area_selection.DisplayedAreaBottomRightHandCorner = [input_dicom.Columns, input_dicom.Rows]
ds_displayed_area_selection.PresentationSizeMode = "SCALE TO FIT"
ds_displayed_area_selection.PresentationPixelAspectRatio = [1, 1]
ds.DisplayedAreaSelectionsSequence = Sequence([ds_displayed_area_selection])

#for ele in input_dicom:
#    ds.add(ele)

'''
#ds.is_little_endian = True
#ds.is_implicit_VR = True


# content desc
ds.ContentDescription = "GSPS"

# gsps study info

# reffer image

# ADD GRAPHIC LAYER
ds_graphic_layer = Dataset()
ds_graphic_layer.GraphicLayer = "Layer1"
ds_graphic_layer.GraphicLayerOrder = 1
ds_graphic_layer.GraphicLayerRecommendedDisplayGrayscaleValue = 65535
ds_graphic_layer.GraphicLayerDescription = "for annotation"

# add display area DisplayedAreaSelections
ds_displayed_area_selection = Dataset()
ds_displayed_area_selection.DisplayedAreaTopLeftHandCorner = [1, 1]
ds_displayed_area_selection.DisplayedAreaBottomRightHandCorner = [input_dicom.Columns, input_dicom.Rows]
ds_displayed_area_selection.PresentationSizeMode = "SCALE TO FIT"
ds_displayed_area_selection.PresentationPixelAspectRatio = [1, 1]

# add circle
ds_cir_object = Dataset()
cir_pos_x, cir_pos_y, cir_rad = 300, 300, 90
ds_cir_object.GraphicAnnotationUnits = "PIXEL"
ds_cir_object.GraphicDimensions = 2
ds_cir_object.NumberOfGraphicPoints = 2
ds_cir_object.GraphicData = [
    cir_pos_x,  # x coordinate of middle of circle
    cir_pos_y,  # y coordinate of middle of circle
    cir_pos_x,  # x coordinate of point on circumference
    cir_pos_y + cir_rad]  # y coordinate of point on circumference
ds_cir_object.GraphicType = "CIRCLE"
ds_cir_object.GraphicFilled = "N"


# add annotation
ds_graphic_annotation = Dataset()
ds_graphic_annotation.GraphicLayer = "Layer1"
ds_graphic_annotation.GraphicObjects = [ds_cir_object]

for ele in ds_graphic_layer:
    ds.add(ele)
for ele in ds_displayed_area_selection:
    ds.add(ele)
for ele in ds_graphic_annotation:
    ds.add(ele)
'''

#ds.is_little_endian = False
#ds.is_implicit_VR = False



print(ds)
ds.save_as("./images/output_sample.dcm")
