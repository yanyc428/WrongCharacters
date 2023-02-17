import pandas as pd


class pinyin(object):
    def __init__(self):
        self.character_dict = pd.read_csv('hanz-pinyin.csv', encoding='gbk', usecols=['ch', 'py'])

    def transform(self, characters):
        for c in characters:
            yield self.character_dict.loc[self.character_dict.ch == c, 'py'].values, c

    def get(self, character):
        s = self.character_dict.loc[self.character_dict.ch == character, 'py'].values
        if len(s) == 0:
            return ''
        return s





