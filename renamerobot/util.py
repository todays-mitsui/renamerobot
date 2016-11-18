# -*- coding: utf-8 -*-

from __future__ import print_function

from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfdocument import  PDFTextExtractionNotAllowed

# import cv2
# import numpy as np
from PIL import Image



def load_pdf(filename, password=None):
    """Open a PDF file."""
    fp = open(filename, 'rb')

    # Create a PDF parser object associated with the file object.
    parser = PDFParser(fp)

    # Create a PDF document object that stores the document structure.
    # Supply the password for initialization.
    document = PDFDocument(parser, password)

    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    return document


def crop(image, ratio_box):
    width, height = image.size
    left, upper, right, lower = ratio_box

    return image.crop((
        left * width,
        upper * height,
        right * width,
        lower * height,
    ))
