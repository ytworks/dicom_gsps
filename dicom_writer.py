#! /usr/bin/env python
# coding:utf-8

from datetime import datetime
import pydicom
from pydicom.dataset import Dataset, DataElement, Tag, FileDataset
from pydicom.sequence import Sequence


def add_circles(dicom, circles, save_file):
    print(dicom)
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.1.1.11.1"  # Grayscale Softcopy Presentation State Storage SOP Class
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.ImplementationClassUID = "1.2.276.0.7230010.3.0.3.4.1"
    file_meta.ImplementationVersionName = "GSPS_DEMO"

    ds_out = FileDataset("sample_annotation", {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds_out.PixelData = dicom.PixelData
    ds_out.save_as(save_file)



def main():
    # load the input image
    input_dicom = pydicom.read_file("./images/sample.dcm")
    print("OK: Read dicom file")

    # test parameter
    cir_rad, cir_pos_x, cir_pos_y = 10, 100, 100
    circles = [{'r' : cir_rad, 'x' : cir_pos_x, 'y' : cir_pos_y}]
    save_file = "./images/sample_annotation.dcm"

    add_circles(input_dicom, circles, save_file)

if __name__ == '__main__':
    main()
