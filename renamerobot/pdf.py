# -*- coding: utf-8 -*-

from __future__ import print_function

import StringIO

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTImage,  LTFigure
from pdfminer.converter import PDFPageAggregator

from PIL import Image



def extract_images(document):
    # Create a PDF resource manager object that stores shared resources.
    rsrcmgr = PDFResourceManager()
    # Create a PDF device object.
    device = PDFPageAggregator(rsrcmgr, laparams=LAParams())
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    contents = []

    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        # print(layout)

        contents.extend(travarse(layout))

    return [to_pil_image(ltImage) for ltImage in contents]


def travarse(layout):
    images = []

    for obj in layout:
        if isinstance(obj, LTTextBox) or isinstance(obj, LTTextLine) or isinstance(obj, LTFigure):
            images.extend(travarse(obj))

        elif isinstance(obj, LTImage):
            images.append(obj)

    return images

def to_pil_image(ltImage):
    buffer = StringIO.StringIO()
    buffer.write(ltImage.stream.get_rawdata())
    buffer.seek(0)
    return Image.open(buffer)
