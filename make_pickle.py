# coding: utf-8
'''
英語と日本語それぞれの、本文とカテゴリをそれぞれリストのpickleとして保存
'''

from __future__ import print_function
import sys
from glob import glob
import re
import numpy as np
import pickle

# 英語と日本語の順序をそろえる。英語ファイルを基準に。
data_dir = './data/corpus_doc'
en_fnames = glob(data_dir + '/en/*.txt')

en_docs = []  # 本文のリスト（英語）
ja_docs = []  # 本文のリスト（日本語）
en_ja_cats = []  # カテゴリラベルのリスト

for en_f in en_fnames:
    mob = re.search(r'([\/\\](\w{3})(\d{5})\.txt)', en_f)
    if mob:
        en_ja_cats.append(mob.group(2))
        en_docs.append(open(en_f, 'r', encoding='utf-8').read())
        ja_f = data_dir + '/ja/' + mob.group(1)  # 同じ名前の日本語ファイル
        try:
            ja_docs.append(open(ja_f, 'r', encoding='utf-8').read())
        except:
            print('no ja file:', mob.group(1), file=sys.stderr)
            sys.exit()
    else:
        print('file name not match', file=sys.stderr)
        sys.exit()

pickle.dump(en_docs, open('./pickles/en_docs.pickle', 'wb'))
pickle.dump(ja_docs, open('./pickles/ja_docs.pickle', 'wb'))
pickle.dump(en_ja_cats, open('./pickles/en_categories.pickle', 'wb'))
pickle.dump(en_ja_cats, open('./pickles/ja_categories.pickle', 'wb'))
