# -*- coding: utf-8 -*-

from __future__ import print_function

from glob import glob
import re
import os
import shutil
from datetime import datetime

from renamerobot.util import load_pdf
from renamerobot.pdf import extract_images
from renamerobot.ocr import read_ordernum, read_date



if not os.path.isdir('BEFORE'):
    os.mkdir('BEFORE')
if not os.path.isdir('AFTER'):
    os.mkdir('AFTER')
if not os.path.isdir(u'読み取り失敗'):
    os.mkdir(u'読み取り失敗')


pdfs = glob('BEFORE/*.pdf')
pdfs_count = len(pdfs)
# print(pdfs)

re_pdfname = re.compile(r'(\\|/)(?P<name>.+)$')

unrenamed = []

for i, pdf in enumerate(pdfs):
    print(u'{0}/{1} 読み取り中 ...'.format(i+1, pdfs_count))

    document = load_pdf(pdf)

    images = extract_images(document)
    ordernum = read_ordernum(images)
    date = read_date(images)

    m = re_pdfname.search(pdf)
    before = m and m.group('name')
    print(u'リネーム前:', before)

    if ordernum is None:
        print(u'  !!受注番号の読み取りに失敗', end='\n\n')
        unrenamed.append(before)
        shutil.copy(pdf, u'読み取り失敗/')

    elif date is None:
        print(u'  !!日付の読み取りに失敗', end='\n\n')
        unrenamed.append(before)
        shutil.copy(pdf, u'読み取り失敗/')

    else:
        after = '{0[ordernum]}_{1[year]:0>4}{1[month]:0>2}{1[day]:0>2}.pdf'.format(ordernum, date)
        print(u'リネーム後:', after, end='\n\n')

        shutil.copyfile(pdf, 'AFTER/'+after)

if 0 != len(unrenamed):
    nowstr = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(u'{1}_【{0}件のリネームできなかったファイル】.txt'.format(len(unrenamed), nowstr), 'w') as f:
        f.write('\n'.join(unrenamed))
