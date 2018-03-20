#!/bin/bash
# xmlファイルから英語最終翻訳文と日本語文を取り出すプログラムmakedata.pyを実行し
# enディレクトリとjaディレクトリにそれぞれファイルを保存

indir=./downloads/wiki_corpus_2.01
outdir=./data/corpus_doc

outdir_en=${outdir%/}/en
outdir_ja=${outdir%/}/ja

mkdir ${outdir}
mkdir ${outdir_en}
mkdir ${outdir_ja}

i=0

find ${indir} -name *.xml | while read inf
do
    fname=${inf##*/}
    fname=${fname%.xml}.txt

    python3 makedata.py ${inf} ${outdir_en}/${fname} ${outdir_ja}/${fname}

    # 1000件ごとに経過を表示
    i=$(expr ${i} + 1)
    if [ $(expr ${i} % 1000) = 0 ]; then
        echo ${i} data done
    fi
done
