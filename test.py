from model import model

test = []
correct = []
with open('test.txt', 'r', encoding='utf-8') as f:
    while True:
        line = f.readline().strip()
        if line:
            test.append(line)
            correct.append(f.readline().strip())
        else:
            break

m = model()
with open('result.txt', 'w', encoding='utf-8') as f:
    for t in test:
        answer = m.merge(t)
        f.write(answer + '\n')
        