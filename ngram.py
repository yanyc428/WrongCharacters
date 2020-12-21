from LAC import LAC


class nGram(object):

    def __init__(self):
        self.lac = LAC(mode='lac')
        self.text = ''
        self.tags = ['PER', 'LOC', 'ORG', 'TIME']
        self.length = 0
        self.seg_text = []

    def seg(self, text):
        self.text = text
        c = self.lac.run(self.text)
        l = []
        for index, tag in enumerate(c[1]):
            if tag in self.tags:
                l.append(c[0][index])
            else:
                l += list(c[0][index])
        self.seg_text = l
        self.length = len(l)

    def ngram(self, text, n=3):
        assert isinstance(text, str)
        assert len(text) > 0
        assert isinstance(n, int)
        self.seg(text)
        print(self.seg_text)
        result = []
        for i in range(self.length - n + 1):
            item = []
            for j in range(n):
                item.append(self.seg_text[i + j])
            result.append(item)
        return result


if __name__ == '__main__':
    ng = nGram()
    print(ng.ngram("程子佳去北师大的乐育超市买小米鸡排"))
