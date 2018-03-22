# coding: utf-8
'''
xmlファイルから英語最終翻訳文と日本語文を取り出してそれぞれファイルに保存
（入出力ディレクトリ名・ファイル名はrun_makedata.shでコントロール）
'''

import sys
from xml.dom import minidom
from normalize_neologd import normalize_neologd

def xml_parse(node, en_sentences, ja_sentences):
    ''' xmlファイルから日本語と英語最終翻訳文を取り出す '''

    if node.nodeType == node.ELEMENT_NODE:
        # 子ノードにeタグ, jタグあれば取り出す
        ch_e_nodes = [ch for ch in node.childNodes if ch.nodeType == ch.ELEMENT_NODE and ch.tagName == 'e']
        ch_j_nodes = [ch for ch in node.childNodes if ch.nodeType == ch.ELEMENT_NODE and ch.tagName == 'j']

        en_sen, ja_sen = '', ''

        # 英語文取り出し
        if len(ch_e_nodes) > 0:

            # eタグの子textnode、3つとも取り出す
            dic_en = {}  # 
            for ch in ch_e_nodes:
                if len(ch.childNodes) == 1 and ch.childNodes[0].nodeType == ch.childNodes[0].TEXT_NODE:
                    dic_en[(ch.getAttribute("type"), ch.getAttribute("ver"))] = ch.childNodes[0].data
                elif len(ch.childNodes) == 0:
                    dic_en[(ch.getAttribute("type"), ch.getAttribute("ver"))] = ''

            # 最終翻訳文を選択
            if ('check', '1') in dic_en:
                en_sen = dic_en[('check', '1')]
            elif ('trans', '2') in dic_en:
                print('warn: en trans 2', file=sys.stderr)
                en_sen = dic_en[('trans', '2')]
            elif ('trans', '1') in dic_en:
                print('warn: en trans 1', file=sys.stderr)
                en_sen = dic_en[('trans', '1')]
            else:
                print('warn: no en', file=sys.stderr)

        # 日本語文取り出し
        if len(ch_j_nodes) > 0:
            if ch_j_nodes[0].childNodes[0].nodeType == ch_j_nodes[0].childNodes[0].TEXT_NODE:
                ja_sen = ch_j_nodes[0].childNodes[0].data
            else:
                print('warn: no ja', file=sys.stderr)
            if len(ch_j_nodes) != 1:
                print('warn: j not 1', file=sys.stderr)

        # 両方そろっていたらappend
        if en_sen and ja_sen:
            en_sentences.append(en_sen)
            ja_sentences.append(ja_sen)

        # 再帰呼び出し
        for child in node.childNodes:
            en_sentences, ja_sentences = xml_parse(child, en_sentences, ja_sentences)

    return en_sentences, ja_sentences


def preproc(*docs):
    ''' 前処理 '''

    prep_docs = []
    for doc in docs:
        # normalize_neologdで正規化
        pp_doc = [normalize_neologd(s) for s in doc]
        # アルファベット大文字を小文字に
        pp_doc = [s.lower() for s in pp_doc]

        prep_docs.append(pp_doc)

    return prep_docs


if __name__ == '__main__':

    infname = sys.argv[1]
    outfname_en = sys.argv[2]
    outfname_ja = sys.argv[3]

    # xmlファイルから日本語と英語最終翻訳文を取り出す
    xdoc = minidom.parse(infname)
    en_doc, ja_doc = xml_parse(xdoc.documentElement, [], [])

    # 前処理(英日)
    en_preproc_doc, ja_preproc_doc = preproc(en_doc, ja_doc)
    
    # ファイル出力
    open(outfname_en, 'w', encoding='utf-8').write('\n'.join(en_preproc_doc))
    open(outfname_ja, 'w', encoding='utf-8').write('\n'.join(ja_preproc_doc))
