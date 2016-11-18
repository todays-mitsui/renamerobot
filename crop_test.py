# -*- coding: utf-8 -*-

from __future__ import print_function

import pprint
pp = pprint.PrettyPrinter(indent=4)

import re
import itertools
from glob import glob

from PIL import ImageOps
from renamerobot.util import load_pdf, crop
from renamerobot.pdf import extract_images


BOXS = {
    'ordernum1': (0.8, 0.11, 0.95, 0.135),
    'ordernum2': (0.8, 0.08, 0.95, 0.105),
    'date1': (0.8, 0.078, 0.95, 0.1),
    'date2': (0.8, 0.06, 0.95, 0.08),
}

def main():
    pdfs = glob('BEFORE/*.pdf')
    pp.pprint(pdfs)

    re_pdfname = re.compile(r'(\\|/)(?P<name>.+)\.pdf')

    for pdf, (box_name, box) in itertools.product(pdfs, BOXS.items()):
        m = re_pdfname.search(pdf)
        pdfname = m and m.group('name')
        print(pdfname)

        document = load_pdf(pdf)
        images = extract_images(document)
        pp.pprint(images)

        for i, image in enumerate(images):
            image = crop(image, box)
            image = ImageOps.grayscale(image)
            # image = resize(image, height=80)
            # image = erode(image)
            image.save('crop_result/{}_{}_{}.gif'.format(pdfname, i, box_name))


if __name__ == '__main__':
    main()
