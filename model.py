from csv import DictReader
import pandas as pd
import numpy as np
from pinyin import pinyin
from ngram import nGram
from visualization import Progress_bar


class model(object):

    def __init__(self):
        self.grams = pd.read_csv('ngram/3gram_1.csv')
        self.py = pinyin()
        self.ng = nGram()
        self.tags = ['PER', 'LOC', 'ORG', 'TIME']
        self.segment = ['，', '。', '？', '！', '：', '；', '……', '【', '】', '（', '）', '“', '”', "《", '》', '、']
        print('init over')

    def seek(self, gram, n=10):
        grams = self.grams[(self.grams.one == gram[0]) & (self.grams.two == gram[1]) & (self.grams.num > n)]
        return grams[['three', 'num']].sort_values(by='num', ascending=False)

    def ngram(self, gram):
        g = self.seek(gram)
        three = np.array(g['three']).tolist()
        if gram[2] in three:
            return True
        return False

    def run(self, text):
        grams = self.ng.ngram(text)
        for index, gram in enumerate(grams):
            if self.ngram(gram):
                yield gram, True
            else:
                yield gram, False

    def merge(self, text):
        res = []
        last = True
        tgs = self.ng.seg(text)

        def trans(txt):
            if txt in self.tags:
                return tgs.pop(0)
            return txt

        for index, t in enumerate(self.run(text)):
            if t[0][0] == 'BOF':
                if index == 0:
                    pass
                else:
                    res[res.index('EOF')] = 'EOFBOF'
                if not last:
                    res.append(')')
                if t[1]:
                    res = res + [trans(t[0][1]), trans(t[0][2])]
                    last = True
                else:
                    res = res + ['('] + [trans(t[0][1]), trans(t[0][2])]
                    last = False
                continue
            if last:
                if t[1]:
                    res.append(trans(t[0][2]))
                    last = True
                else:
                    if res[-2] == ')':
                        res = res[:-1] + ['('] + res[-1:] + [trans(t[0][2])]
                    else:
                        res = res[:-2] + ['('] + res[-2:] + [trans(t[0][2])]
                    last = False
            else:
                if t[1]:
                    res.append(')')
                    res.append(trans(t[0][2]))
                    last = True
                else:
                    res.append(trans(t[0][2]))
                    last = False

            print(res)

        if not last:
            res.append(')')
        # biao dian
        seg = []
        for i in text:
            if i in self.segment:
                seg.append(i)

        for index, item in enumerate(res):
            if (item == 'EOFBOF') | (item == 'EOF'):
                res[index] = seg.pop(0)
            elif item == 'BOF':
                res[index] = ''

        return ''.join(res)

    def correct(self, gram, n=10):
        print('start')
        one = self.grams[(self.grams.three == gram[2]) & (self.grams.two == gram[1]) & (self.grams.num > n)]
        two = self.grams[(self.grams.one == gram[0]) & (self.grams.three == gram[2]) & (self.grams.num > n)]
        three = self.grams[(self.grams.one == gram[0]) & (self.grams.two == gram[1]) & (self.grams.num > n)]

        data = pd.concat([one, two, three]).sort_values(by='num', ascending=False)

        one_py = self.py.get(gram[0])[0]
        two_py = self.py.get(gram[1])[0]
        three_py = self.py.get(gram[2])[0]

        for index, d in data.iterrows():
            if (one_py in self.py.get(d['one'])) & (two_py in self.py.get(d['two'])) & (
                    three_py in self.py.get(d['three'])):
                return [d['one'], d['two'], d['three']]
        return gram


if __name__ == '__main__':
    m = model()
    # print(m.merge('禁日，陆军某综合训练鸡地新兵结业表张大会上，有这样两个身影银起大家的注意，他们就是11连的连长和旨导员。'))
    # print(m.merge('新的一粘，是我国完成“九五”计划和本世纪膜奋斗目标的重要年分，改革、发展和稳定的任务十分繁重。为更好的报到改革发展进程中的新气象、新成就，在新的一年众，本报将对有关拌面进行调整。'))
    # print(m.merge('今年以来，自治区当委、政府多次召开专门会议，研究项目落实问题。对余资金未到位的，自治区朱要领导亲自出面，与国内外客商恰谈，介绍宁夏的投资环境，从而使许多项目落到了实处。目前，宁夏外商投资项目资今到位率居全国中上水平。'))
    # print(m.merge('11月上旬，江阴长江大桥刚刚通扯，地处北岸的江苏省泰州市就在全市范围内绽开了“大桥通车和泰州经济发展鸡遇”的讨论。经过套论，全市人民达成共事：泰州要抓住大翘通车机遇，主动接受上海和苏南等发达地区的经济富射，全面推进大开放站略，带动和促进泰州经济的全面发展。'))
    # print(m.merge('和评发展，是深刻把握时代特征、中国国情，统筹国内国际两哥大局，借鉴、汲取他国发战经验，做出的重大战略抉择，也是中国对歪战略的正重宣誓。'))
    # print(m.merge('环境正洁、交通遍利是一个城市更加开放的“硬件”标志。泰州是大力加强区域中心城市建设，在“完善功能，改善环境，提高品位，树里形象”上下功夫，着重在水、路、房等方面进行集中投入，重点减设。先后完成一水厂水源水质整治和7条城市河道的疏俊和环境综合整治，有效地盖善了市区内河道的环境面貌。'))
    print(m.merge('另据报到，24日晚，刚刚下台的钱总理斯捷帕申决定与“亚博卢”集团节盟，参加12月的杜马竟选。但斯捷帕申表示，他不加入“亚博卢”及团。'))
    # print(m.merge('俄内务补临时新闻中心说，俄军这次围教的目标是达吉斯坦布伊纳克斯基区的卡拉马希村和恰班马希村。'))
    # print(m.merge('我认识一位叔叔，是个吻学爱好者，梦想是成为一名做家。他曾写作近十年，但除了在杂志上零兴发表一些文章外，几乎没有什么更好的橙绩。'))
    # print(m.merge('常有人说，理想很风满，现实很骨感。有石候，我们也会抱怨付出不一腚有回报、努力不一定有结果。此时如果发现了自己新的钱力，不妨试着换一个方向继续努利。'))
    # print(m.correct(['很', '风', '满']))
    # print(m.correct(['吻', '学', '爱']))
    # print(m.correct(['内', '务', '补']))
    # print(m.correct(['据', '报', '到']))
    # print(m.correct(['通', '遍', '利']))
    # print(m.correct(['和', '评', '发']))
    # print(m.correct(['刚', '通', '扯']))
    # print(m.correct(['对', '余', '资']))
    # print(m.correct(['区', '当', '委']))
    # print(m.correct(['旨', '导', '员']))

