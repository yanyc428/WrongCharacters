from LAC import LAC

# 装载分词模型
lac = LAC(mode='lac')

# 单个样本输入，输入为Unicode编码的字符串
text = u"LAC是个优秀的分词工具"
seg_result = lac.run(text)
print(seg_result)


# 批量样本输入, 输入为多个句子组成的list，平均速率会更快
texts = [u"程子佳喜欢肖明"]
seg_result = lac.run(texts)
print(seg_result)


texts = [u"程子佳去北师大的乐育超市买小米鸡排"]
seg_result = lac.run(texts)
print(seg_result)


texts = [u"习近平是习远平的哥哥"]
seg_result = lac.run(texts)
print(seg_result)