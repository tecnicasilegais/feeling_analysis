import numpy.random as rnd
import locale

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

filename = "test.txt"

bgw = 30

positive_sentences = []
negative_sentences = []

bow = []


class Sent:
    def __init__(self):
        self.type = None  # class
        self.id = None  # id
        self.words = None  # words list


def read_dataset():
    objs = open(filename, 'r', encoding='utf-8').read().split('<end>')
    for o in objs:
        lines = o.strip().splitlines()
        s = Sent()
        s.type = lines[0].replace('<class>', '').replace('</class>', '').strip()
        s.id = lines[1].replace('<id>', '').replace('</id>', '').strip()
        s.words = []
        for word in lines[2:]:
            s.words.append(word.split('   ')[1].strip())
        if s.type == '1':
            positive_sentences.append(s)
        else:
            negative_sentences.append(s)


def count_words(lst):
    dt = dict()
    for s in lst:
        for w in s.words:
            if w in dt:
                dt[w] = (w, dt[w][1]+1)
            else:
                dt[w] = (w, 1)
    return list(dt.values())


def select_words(words_tuple):
    global bgw
    words_tuple.sort(key=lambda t: t[1], reverse=True)
    words = [t[0] for t in words_tuple[:30]]
    return set(words)


def create_arff():
    positive_training_len = int((len(positive_sentences) * 80)/100)
    negative_training_len = int((len(negative_sentences) * 80)/100)
    rnd.shuffle(positive_sentences)
    rnd.shuffle(negative_sentences)
    handle_arff(positive_sentences[:positive_training_len], negative_sentences[:negative_training_len], "training.arff")
    handle_arff(positive_sentences[positive_training_len:], negative_sentences[negative_training_len:], "testing.arff")


def write_sentences_arff(sentences, f):
    for sent in sentences:
        for word in bow:
            if word in sent.words:
                f.write(str(1)+',')
            else:
                f.write(str(0)+',')
        if sent.type == '1':
            f.write('positive\n')
        else:
            f.write('negative\n')


def handle_arff(p_sentences, n_sentences, f_name):
    global bow
    f = open(f_name, 'w', encoding='utf-8')
    f.write('@relation feelingAnalysis\n\n')    # relation

    for word in bow:
        f.write('@attribute %s numeric\n' % word)   # attributes
    f.write('@attribute class {positive, negative}\n\n@data\n')

    write_sentences_arff(p_sentences, f)
    write_sentences_arff(n_sentences, f)


def main():
    global bow
    read_dataset()
    positive_words = count_words(positive_sentences)
    negative_words = count_words(negative_sentences)

    spw = select_words(positive_words)
    snw = select_words(negative_words)

    bow = list(set(spw.union(snw)))
    create_arff()


if __name__ == '__main__':
    main()
