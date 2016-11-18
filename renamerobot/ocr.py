# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import itertools
import re

import pyocr
import pyocr.builders
from renamerobot.util import crop

from PIL import ImageOps


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]


ORDERNUM_BOX = (
    (0.8, 0.11, 0.95, 0.135),
    (0.8, 0.08, 0.95, 0.105),
)

re_ordernum = re.compile(r'(?P<num>\d{4,})$', re.MULTILINE)

REPLACE_PAIR_1 = (
    (u']', u'1'),
    (u'}', u'1'),
    (u'ー', u'1'),
    (u'Z', u'2'),
    (u'O', u'0'),
    (u'〇', u'0'),
    (u'I', u'1'),
    (u'l', u'1'),
)

def read_ordernum(images):
    for image, box in itertools.product(images, ORDERNUM_BOX):
        image = crop(image, box)
        image = ImageOps.grayscale(image)
        # image = resize(image, height=80)
        # image = erode(image)

        txt = tool.image_to_string(
            image,
            lang='eng',
            builder=pyocr.builders.TextBuilder(tesseract_layout=7)
        )

        for before, after in REPLACE_PAIR_1:
            txt = txt.replace(before, after)
        txt = re.sub(r'\s+', '', txt)

        # try:
        #     print('OCR:')
        #     print(txt)
        # except Exception as e:
        #     print(e)

        result = re_ordernum.search(txt)

        if result is not None:
            return {
                'ordernum': result.group('num'),
            }

    return None


DATE_BOX = (
    (0.8, 0.078, 0.95, 0.1),
    (0.8, 0.06, 0.95, 0.08),
)

re_date = re.compile(u'(?P<year>\\d{4})年(?P<month>\\d{1,2})月(?P<day>\\d{1,2})日', re.MULTILINE)

REPLACE_PAIR_2 = (
    (u']', u'1'),
    (u'}', u'1'),
    (u'ー', u'1'),
    (u'仔', u'年'),
    (u'El', u'日'),
    (u'E|', u'日'),
    (u'E', u'日'),
    (u'□', u'日'),
    (u'口', u'日'),
    (u'曰', u'日'),
    (u'Z', u'2'),
    (u'O', u'0'),
    (u'〇', u'0'),
    (u'I', u'1'),
    (u'l', u'1'),
)

def read_date(images):
    for image, box in itertools.product(images, DATE_BOX):
        image = crop(image, box)
        image = ImageOps.grayscale(image)
        # image = resize(image, height=80)
        # image = erode(image)

        txt = tool.image_to_string(
            image,
            lang='jpn+eng',
            builder=pyocr.builders.TextBuilder(tesseract_layout=6)
        )

        for before, after in REPLACE_PAIR_2:
            txt = txt.replace(before, after)
        txt = re.sub(r'\s+', '', txt)

        # try:
        #     print('OCR:')
        #     print(txt)
        # except Exception as e:
        #     print(e)

        result = re_date.search(txt)

        if result is not None:
            return {
                'year': result.group('year'),
                'month': result.group('month'),
                'day': result.group('day'),
            }

    return None
