
f = open("eng-ita_original.txt","r", encoding="utf-8")
line = f.readlines()
#print(line)
new_line = []
#line[i]で、'\tCC-BY'という文字列が現れたら以降の文字は削除
for i in range(0, len(line)):
  s = str(line[i])
  target = '\tCC-BY'
  idx = s.find(target)
  r = s[:idx]
  new_line.append(r)
#print(new_line)

ff = open('eng-ita.txt', 'w', encoding="utf-8")
ff.writelines([w + '\n' for w in new_line])
ff.close()