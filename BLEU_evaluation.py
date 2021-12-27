# https://mtmt-nlp.com/?p=336
# -*- coding:utf-8 -*-

import nltk
from nltk.translate.bleu_score import SmoothingFunction

f = open("data/for_evaluation/eng-fra_output_pred(eng).txt", "r")  # 出力
f2 = open("data/for_evaluation/eng-fra_output(eng).txt", "r")  # 正解

a = f.read()
li = a.split("\n")
a2 = f2.read()
li2 = a2.split("\n")

s = 0.0

chencherry = SmoothingFunction()

for i2 in range(100):  # 文書数100の場合
    hy = []
    re = []
    hy = li[i2].split(" ")
    re = li2[i2].split(" ")
    if not len(hy) == 1:
        s = s + nltk.translate.bleu_score.sentence_bleu([re], hy, smoothing_function=chencherry.method4)

print("BLEU:")
print(s / 1000)