import random

f = open("eng-fra.txt","r", encoding="utf-8")
line = f.readlines()
#print(line)
input_line = []
corect_output_line = []
#line[i]で、'\t'という文字が現れたらそれ以前（input_line）と以降(correct_output_line)で分割
for i in range(0, len(line)):
  s = str(line[i])
  target = '\t'
  idx = s.find(target)
  r0 = s[:idx]
  r1 = s[idx+1:]
  input_line.append(r0)
  corect_output_line.append(r1)
input_line = random.sample(input_line, 100)
corect_output_line = random.sample(corect_output_line, 100)

f1 = open('eng-fra_input(fra).txt', 'w', encoding="utf-8")
f1.writelines([w for w in corect_output_line])
f1.close()

f2 = open('eng-fra_output(eng).txt', 'w', encoding="utf-8")
f2.writelines([w + '\n' for w in input_line])
f2.close()