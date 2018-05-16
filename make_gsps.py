#! /usr/bin/env python
# coding:utf-8
import pydicom as dicom
import os
from pydicom.dataset import Dataset, FileDataset
from pydicom.sequence import Sequence
from shutil import copyfile
from datetime import datetime
import json


def generate(input_file, json_file, output_file):
    input_dicom = dicom.read_file(input_file)
    dataset = Dataset()
    dataset = __make_file(dataset, output_file)
    dataset = __basic_settings_for_gsps(dataset)
    dataset = __copy_from_original(dataset, input_dicom)
    dataset.save_as(output_file)
    return dataset


def __copy_from_original(dataset, input_dicom):
    data_elements = ['PatientID',
                     'PatientBirthDate',
                     'StudyInstanceUID',
                     'StudyDescription',
                     'PatientName',
                     'PatientSex',
                     'StudyID',
                     'StudyDate',
                     'StudyTime',
                     'ReferringPhysicianName',
                     'AccessionNumber']
    for de in input_dicom:
        print(de)
        if de.name in data_elements:
            dataset.add(input_file.data_element(de.name))
    return dataset

def __basic_settings_for_gsps(dataset):
    dataset.SOPClassUID = "Grayscale Softcopy Presentation State Storage"
    dataset.SOPInstanceUID = dicom.uid.generate_uid()
    dataset.Modality = "PR"
    return dataset

def __add_annotation(dataset, json_file):
    annotation_data = json.load(json_file)
    print(annotation_data)

def __make_file(dataset, output_file):
    ds = FileDataset(os.path.basename(output_file), {},
                     file_meta=dataset,
                     preamble=b"\0" * 128)
    return ds


def test():
    dcm = generate(input_file = "./images/sample.dcm",
             json_file = "./images/sample.json",
             output_file = "./images/output_sample.dcm")
    print(dcm)

if __name__=='__main__':
    test()
