from LAC import LAC


class nGram(object):

    def __init__(self):
        self.lac = LAC(mode='lac')
        self.text = ''
        self.tags = ['PER', 'LOC', 'ORG', 'TIME']
        self.length = 0
        self.seg_text = []
        self.segment = ['，', '。', '？', '！', '：', '；', '……', '【', '】', '（', '）', '“', '”', "《", '》', '、']
        self.stop = []

    def seg(self, text):
        self.text = text
        c = self.lac.run(self.text)
        l = []
        for index, tag in enumerate(c[1]):
            if tag in self.tags:
                self.stop.append(c[0][index])
                l.append(tag)
            else:
                l += list(c[0][index])
        self.seg_text = l
        self.length = len(l)

    def ngram(self, text, n=3):
        assert isinstance(text, str)
        assert len(text) > 0
        assert isinstance(n, int)
        self.seg(text)
        for i in range(-1, self.length - n + 2):
            item = []
            for j in range(n):
                if i + j == -1:
                    item.append('BOF')
                elif i + j == self.length:
                    item.append('EOF')
                elif self.seg_text[i + j] in self.segment:
                    if j == 0:
                        item.append('BOF')
                    elif j == n - 1:
                        item.append('EOF')
                    else:
                        break
                else:
                    item.append(self.seg_text[i + j])
            if len(item) == n:
                yield item


if __name__ == '__main__':
    ng = nGram()
    s = "程子佳去北师大的“乐育超市”买【小米鸡排】，小米鸡排、汉堡包真的很好吃"
    for item in ng.ngram(s):
        s = "程子佳去北师大的“超市”买【小米鸡排】，小米鸡排、汉堡包真的很好吃"
        print(item)

