import pandas as pd
import random


class WrongGenerate(object):

    def __init__(self):
        self.character_dict = pd.read_csv('hanz-pinyin.csv', encoding='gbk', usecols=['ch', 'py'])
        self.segment = ['，', '。', '？', '！', '：', '；', '……', '【', '】', '（', '）', '“', '”', "《", '》', '、', '1', '2', '3',
                        '4', '5', '6', '7', '8', '9', '0']

    def generate(self, text, mode=True, rate=0.05):
        assert mode in [True, False]
        assert (float(rate) >= 0) & (float(rate) <= 1)
        text = text.replace(' ', '')
        length = len(text)
        indices = []
        for i in range(int(length * rate)):
            indices.append(random.randint(0, length))
        for index in indices:
            raw = text[index]
            if raw in self.segment:
                continue
            raw_py = self.character_dict.loc[self.character_dict.ch == raw, 'py'].values
            wrong_cell = self.character_dict.loc[self.character_dict.py == raw_py[0], 'ch'].values
            wrong = random.choice(wrong_cell)
            text = text[0:index] + wrong + text[index + 1:]
        return text


if __name__ == '__main__':
    g = WrongGenerate()
    print(g.generate(
        "新华社北京12月21日电  （刘济美、吴旭）中央军委主席习近平日前签署命令，发布《军队军事职业教育条例（试行）》（以下简称《条例》），自2021年1月1"
        "日起施行。《条例》深入贯彻习近平强军思想，深入贯彻新时代军事教育方针，围绕培养德才兼备的高素质、专业化新型军事人才，着眼构建形成时时学、处处学"
        "、人人学、终身学的格局，坚持正确政治方向，坚持紧贴使命任务、岗位履职、职业发展，完善网络化、开放式、全覆盖军事职业教育体系，从宏观上"
        "建立军事职业教育制度机制，对于推动军事职业教育建设发展、构建新型军事人才培养体系，具有重要意义。《条例》共8章43条，界定了军事职业"
        "教育对象范围、组织形式、时代要求等基本内涵，构建了中央军委统一领导下的军事职业教育领导管理体系，对教育任务、学习管理、支撑保障、"
        "激励与监督等内容作了系统规范，为激发官兵学习动力、规范工作管理运行提供了有力制度保证。", rate=0.2))
