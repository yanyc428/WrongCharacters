from csv import DictReader
import pandas as pd
import numpy as np
from pinyin import pinyin
from ngram import nGram
from visualization import Progress_bar


class model(object):

    def __init__(self):
        self.grams = pd.read_csv('3gram.csv')
        self.py = pinyin()
        self.ng = nGram()
        self.segment = ['，', '。', '？', '！', '：', '；', '……', '【', '】', '（', '）', '“', '”', "《", '》', '、']
        print('init over')

    def seek(self, gram, n=10):
        grams = self.grams[(self.grams.one == gram[0]) & (self.grams.two == gram[1]) & (self.grams.num > n)]
        return grams[['three', 'num']].sort_values(by='num', ascending=False)

    def ngram(self, gram):
        g = self.seek(gram)
        three = np.array(g['three']).tolist()
        if gram[2] in three:
            return gram
        p = self.py.get(gram[2])
        for t1, t2 in self.py.transform(three):
            if p in t1:
                return [gram[0], gram[1], t2]
        return gram

    def run(self, text):
        grams = self.ng.ngram(text)
        print(grams)
        n = 0
        for index, gram in enumerate(grams):
            if n > 0:
                n -= 1
                yield gram
                continue
            if gram[2] != self.ngram(gram)[2]:
                n += 2
            yield self.ngram(gram)

    def get(self, text):
        print("start\n")
        seg = []
        for i in text:
            if i in self.segment:
                seg.append(i)
        res = ['']
        for i, r in enumerate(self.run(text)):
            if r[0] == 'BOF':
                if res[-1] == 'EOF':
                    res[-1] = 'EOFBOF'
                    res = res + r[1:]
                else:
                    res = res + r
            else:
                res.append(r[-1])
            print("process:", r)
        for index, item in enumerate(res):
            if (item == 'EOFBOF') | (item == 'EOF'):
                res[index] = seg.pop(0)
            elif item == 'BOF':
                res[index] = ''
        print('stop\n')
        return ''.join(res)


if __name__ == '__main__':
    from generate_wrong import WrongGenerate
    wg = WrongGenerate()
    s = "中国不今有继续扩大开放的决心吗，还推出了许多具体政策措使。比如，全面实施外商投资法及其实施条李，进一步缩减外商投资准入负面清单，" \
        "稳步推动金容市场准入，出台海南自由贸易港建设总提方案，强化深圳和浦东的改革开放举错，深化服务贸一创新发展试点等。"
    ws = wg.generate(s)
    m = model()
    print(m.get(s))
