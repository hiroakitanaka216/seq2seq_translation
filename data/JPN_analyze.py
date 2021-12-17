from janome.tokenizer import Tokenizer

ff = open('eng-jpn-0.txt', 'r', encoding="utf-8")
line = ff.readlines()

jpn_line = []
eng_line = []

#line[i]で、'\t'の手前は英語、後ろは日本語でそれぞれを分割
for i in range(0, len(line)):
  s = str(line[i])
  target = '\t'
  idx = s.find(target)
  e = s[:idx]
  j = s[idx+1:-1]
  eng_line.append(e)
  jpn_line.append(j)
#print(eng_line)
#print(jpn_line)

t = Tokenizer()
jpn_analyze_list = []
new_jpn_line = []
for j in range(0, len(jpn_line)):
  s1 = str(jpn_line[j])
  jpn_analyze_list.append([token.surface for token in t.tokenize(s1)]) #jpn_analyze_list[文章番号][形態素番号]

#print(jpn_analyze_list[1990])

for k in range(0, len(jpn_line)):
  s2 = ' '.join(jpn_analyze_list[k])
  new_jpn_line.append(s2)
#print(new_jpn_line)

new_line = []

for l in range(0, len(jpn_line)):
  sj = str(new_jpn_line[l])
  se = str(eng_line[l])
  new_line.append(se+'\t'+sj)

ff = open('eng-jpn.txt', 'w', encoding="utf-8")
ff.writelines([w + '\n' for w in new_line])
ff.close()