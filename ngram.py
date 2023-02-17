from LAC import LAC


class nGram(object):

    def __init__(self):
        self.lac = LAC(mode='lac')
        self.text = ''
        self.tags = ['PER', 'LOC', 'ORG', 'TIME']
        self.length = 0
        self.seg_text = []
        self.segment = ['，', '。', '？', '！', '：', '；', '……', '【', '】', '（', '）', '“', '”', "《", '》', '、']

    def seg(self, text):
        stop = []
        self.text = text
        c = self.lac.run(self.text)
        l = []
        for index, tag in enumerate(c[1]):
            if tag in self.tags:
                stop.append(c[0][index])
                l.append(tag)
            else:
                l += list(c[0][index])
        self.seg_text = l
        self.length = len(l)
        return stop

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
    s = "另据报到，24日晚，刚刚下台的钱总理斯捷帕申决定与“亚博卢”集团节盟，参加12月的杜马竟选。但斯捷帕申表示，他不加入“亚博卢”及团。"
    for item in ng.ngram(s):
        print(item)
