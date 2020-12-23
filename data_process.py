import os
import csv


class NGramGenerator:
    def __init__(self, n):
        self.base_dir = 'ngram'
        if not os.path.exists(self.base_dir):
            os.mkdir(self.base_dir)
        self.path = os.path.join(self.base_dir, str(n) + 'gram_1.csv')
        self.dic = {}
        self.headers = ['one', 'two', 'three', 'num']

    def generate(self, grams):
        for gram in grams:
            self.dic.setdefault((gram[0], gram[1], gram[2]), 1)
            self.dic[(gram[0], gram[1], gram[2])] += 1

    def save(self):
        bar = Progress_bar()
        with open(self.path, 'w+', newline='', encoding='utf-8') as f:
            f_csv = csv.DictWriter(f, self.headers)
            f_csv.writeheader()
            length = len(self.dic.keys())
            for i, key in enumerate(self.dic.keys()):
                f_csv.writerow({'one': key[0], 'two': key[1], 'three': key[2], 'num': self.dic[key]})
                bar.bar(i, length, "Preprocessed ")
        print("\nfinish write: " + self.path)


if __name__ == '__main__':
    from ngram import nGram
    from visualization import Progress_bar

    ng = nGram()
    ngg = NGramGenerator(3)

    file_dir = 'raw_data'

    for files in os.listdir(file_dir)[-10:]:
        b = Progress_bar()
        with open(os.path.join(file_dir, files), 'r', encoding='utf-8') as f:
            data = f.read().split()
            l = len(data)
            for index, d in enumerate(data):
                gs = ng.ngram(d)
                ngg.generate(gs)
                b.bar(index, l, "Preprocessed " + files)
        print("\nfinish index: " + files)
    ngg.save()
