# https://mtmt-nlp.com/?p=336
# -*- coding:utf-8 -*-

import nltk
from nltk.translate.bleu_score import SmoothingFunction

#f = open("eng-fra_output_pred(eng)_epoch12500_GRU.txt", "r")  # 出力１
f = open("eng-fra_output_pred(eng)_epoch4000_RNN.txt", "r")  # 出力２
#f = open("eng-fra_output_pred(eng)_DeepL.txt", "r")  # 出力３
#f = open("eng-fra_output_pred(eng)_GoogleTranslation.txt", "r")  # 出力４
f2 = open("eng-fra_output_correct(eng).txt", "r")  # 正解

a = f.read()
li = a.split("\n")
a2 = f2.read()
li2 = a2.split("\n")

s = 0.0

chencherry = SmoothingFunction()

for i2 in range(len(li)):  # 文書数100の場合
    hy = []
    re = []
    hy = li[i2].split(" ")
    re = li2[i2].split(" ")
    if not len(hy) == 1:
        s = s + nltk.translate.bleu_score.sentence_bleu([re], hy, smoothing_function=chencherry.method4)

print("BLEU:")
print(s / len(li))