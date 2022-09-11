import random
import re as re
import collections as Co


def text_to_corpus():
    text = open('pushkin.txt', encoding='utf-8').read()
    text = text.lower()
    text = re.sub(r'<>"*[0-9().,?:;!-]', '', text)
    corpus = text.split()
    return corpus


def bi_dict(corpus):
    len_corpus = len(corpus)

    bf_dict = Co.defaultdict()
    nd = Co.defaultdict()
    for i in range(0, len_corpus - 1):
        count = bf_dict.get((corpus[i], corpus[i + 1]), 0)
        bf_dict[(corpus[i], corpus[i + 1])] = (
                count + 1)  # Составили словарь bf_dict из биграмм и для каждой биграммы посчитали их количество
    for key in bf_dict:
        word = key[0]
        if nd.get(word) is None:
            nd[word] = (key[1],)
        else:
            nd[word] = nd[word] + (
                key[1],)  # Составили словарь nd из слов, которые могут следовать за словом на обучающей выборке
    for key in nd:
        count = 0
        for sec in nd[key]:
            count += bf_dict.get((key, sec))
        for sec in nd[key]:
            bf_dict[(key, sec)] = bf_dict.get((key, sec)) / count  # Нормировка для вероятности

    return nd, bf_dict


def generateText(n, nd, bf_dict,
                 seed='NetNF'):  # В процессе генерации текста выбирается случайное слово из словаря биграмм с той вероятностью,
    if seed == 'NetNF':          # которая была у такой пары при обучении
        seed = corpus[random.choice(range(0, len(corpus)))]

    seq = (seed,)
    for i in range(0, n - 1):
        lastw = seq[i]
        pw = random.random()
        pcount = 0
        for sec in nd[lastw]:
            pcount += bf_dict[(lastw, sec)]
            if pcount >= pw:
                nextword = sec
                break
        seq = seq + (nextword,)

    return seq


def printText(seq):
    gtext = ''
    for word in seq:
        gtext = gtext + ' ' + word
    return gtext


corpus = text_to_corpus()
bd = bi_dict(corpus)
nd = bd[0]
bf_dict = bd[1]

n = 20  # Количество генерируемых слов
seq = generateText(n, nd, bf_dict)

print(printText(seq))
