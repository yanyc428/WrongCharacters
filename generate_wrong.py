import pandas as pd
import random


class WrongGenerate(object):

    def __init__(self):
        self.character_dict = pd.read_csv('hanz-pinyin.csv', encoding='gbk', usecols=['ch', 'py'])

    def generate(self, text, mode=True, rate=0.05):
        assert mode in [True, False]
        assert (float(rate) >= 0) & (float(rate) <= 1)
        length = len(text)
        indices = []
        for i in range(int(length * rate)):
            indices.append(random.randint(0, length))
        for index in indices:
            raw = text[index]
            raw_py = self.character_dict.loc[self.character_dict.ch == raw, 'py'].values
            wrong_cell = self.character_dict.loc[self.character_dict.py == raw_py[0], 'ch'].values
            wrong = random.choice(wrong_cell)
            text = text[0:index] + wrong + text[index+1:]
        return text


if __name__ == '__main__':
    g = WrongGenerate()
    print(g.generate("程子佳去北师大的乐育超市买小米鸡排", rate=0.2))
