#! /usr/bin/env python
# coding:utf-8
import pydicom as dicom
import os
from pydicom.dataset import Dataset, FileDataset
from pydicom.sequence import Sequence
from shutil import copyfile
from datetime import datetime
import json
import codecs


def generate(input_file, json_file, output_file):
    input_dicom = dicom.read_file(input_file)
    dataset = Dataset()
    dataset = __make_file(dataset, output_file)
    dataset = __basic_settings_for_gsps(dataset)
    dataset = __add_referrence(dataset, input_dicom)
    dataset = __copy_from_original(dataset, input_dicom)
    dataset = __add_annotation(dataset, json_file, input_dicom)
    dataset.save_as(output_file)
    return dataset


def __img_object(input_dicom):
    img = Dataset()
    img.SOPClassUID = input_dicom.SOPClassUID
    img.SOPInstanceUID = input_dicom.SOPInstanceUID
    return img


def __add_referrence(dataset, input_dicom):
    rss = Dataset()
    img = __img_object(input_dicom)
    rss.ReferencedImageSequence = Sequence([img])
    dataset.ReferencedSeriesSequence = Sequence([rss])
    return dataset


def __copy_from_original(dataset, input_dicom):
    data_elements = ['Patient ID',
                     'Patient\'s Birth Date',
                     'Study Instance UID',
                     'Study Description',
                     'Patient Name',
                     'Patient Sex',
                     'Study ID',
                     'Study Date',
                     'Study Time',
                     'Referring Physician Name',
                     'Accession Number',
                     'Series Instance UID']
    for de in input_dicom:
        if de.name in data_elements:
            dataset.add(de)
    return dataset


def __basic_settings_for_gsps(dataset):
    dataset.SOPClassUID = "Grayscale Softcopy Presentation State Storage"
    dataset.SOPInstanceUID = dicom.uid.generate_uid()
    dataset.Modality = "PR"
    return dataset


def __add_annotation(dataset, json_file, input_dicom):
    dataset = __add_display_area(dataset, input_dicom)
    f = open(json_file, 'r')
    annotation_data = json.load(f)
    layer_objects = []
    for layer, circles in annotation_data.items():
        layer_objects.append(__add_layer(dataset, {layer : circles}, input_dicom))
    dataset.GraphicAnnotationSequence = Sequence(layer_objects)
    return dataset

def __add_layer(dataset, layer, input_dicom):
    layer_object = Dataset()
    layer_object.GraphicLayer = layer.keys()[0]
    img = __img_object(input_dicom)
    layer_object.ReferencedImageSequence = Sequence([img])
    layer_object = __add_circles(layer_object, layer.values()[0])
    return layer_object

def __add_circles(dataset, circles):
    circle_objects = []
    for circle in circles:
        ds_cir_object = Dataset()
        cir_pos_x = circle['x']
        cir_pos_y = circle['y']
        cir_rad = circle['radius']
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
        circle_objects.append(ds_cir_object)
    dataset.GraphicObjectSequence = Sequence(circle_objects)
    return dataset

def __add_display_area(dataset, input_dicom):
    ds_displayed_area_selection = Dataset()
    ds_displayed_area_selection.DisplayedAreaTopLeftHandCorner = [1, 1]
    ds_displayed_area_selection.DisplayedAreaBottomRightHandCorner = [input_dicom.Columns, input_dicom.Rows]
    ds_displayed_area_selection.PresentationSizeMode = "SCALE TO FIT"
    ds_displayed_area_selection.PresentationPixelAspectRatio = [1, 1]
    dataset.DisplayedAreaSelectionSequence = Sequence([ds_displayed_area_selection])
    return dataset

def __make_file(dataset, output_file):
    ds = FileDataset(os.path.basename(output_file), {},
                     file_meta=dataset,
                     preamble=b"\0" * 128)
    return ds


def test():
    __make_sample()
    dcm = generate(input_file="./images/sample.dcm",
                   json_file="./images/sample.json",
                   output_file="./images/output_sample.dcm")
    print(dcm)


def __make_sample():
    data = {"A": [{"radius": 10, "x": 100, "y": 100},
                  {"radius": 10, "x": 200, "y": 100}],
            "B": [{"radius": 10, "x": 100, "y": 200},
                  {"radius": 10, "x": 200, "y": 200}]
            }
    json.dump(data, open("./images/sample.json", 'w'), indent=4)

if __name__ == '__main__':
    test()
