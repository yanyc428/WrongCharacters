import os

raw_data = "./raw_data"


def get_passage():
    for item in os.listdir(raw_data):
        with open(os.path.join(raw_data, item), "r", encoding="utf-8") as f:
            yield f.read()


if __name__ == '__main__':
    for index, x in enumerate(get_passage()):
        if index < 2:
            print(index, x[0:10])
        else:
            break
