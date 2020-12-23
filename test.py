# import pandas as pd
#
# data = pd.read_csv('ngram/3gram.csv')
#
# print(data)
#
# print(data[(data.one == '京') & (data.two == '剧')])
from LAC import LAC

l = LAC()

print(l.run("中国不今有继续扩大开放的决心，还推出了许多具体政策措使。比如，全面实施外商投资法及其实施条李，进一步缩减外商投资准入负面清单，"
      "稳步推动金容市场准入，出台海南自由贸易港建设总提方案，强化深圳和浦东的改革开放举错，深化服务贸一创新发展试点等。"))


import jieba

print(list(jieba.cut("中国不今有继续扩大开放的决心，还推出了许多具体政策措使。比如，全面实施外商投资法及其实施条李，进一步缩减外商投资准入负面清单，"
      "稳步推动金容市场准入，出台海南自由贸易港建设总提方案，强化深圳和浦东的改革开放举错，深化服务贸一创新发展试点等。")))