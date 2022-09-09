import pprint
import re
import os
import json
import argparse
import sys


class Ngrams:
    def __init__(self):
        if 'model.json' not in os.listdir():
            self.iternal_start()
        self.tmp = {}

    def fit(self, text=None, file=None):
        self.get_data()
        if file:
            files = [i for i in os.listdir(file)]
            for path in files:
                self.make_corpus(path=file + '\\' + path)
        if text:
            self.make_corpus(text=text)
        out = open('model.json', 'w')
        json.dump(self.tmp, out)

    def make_corpus(self, text=None, path=None):
        for token_length in range(1, 6):
            if text:
                tokens = self.tokenization(txt=text, n=token_length)
            if path:
                tokens = self.tokenization(filename=path, n=token_length)

            if token_length == 1:
                if tokens[1] not in self.tmp['books']:
                    self.tmp['books'].append(tokens[1])
            # if token_length == 2:
            #     print(token_length, tokens[0])
            self.update_data(tokens=tokens[0], length=str(token_length))

    def update_data(self, tokens, length):
        # print(tokens)
        for i in range(len(tokens)-1):
            # print(tokens[i], tokens[i+1])
            current_word = ' '.join(tokens[i])
            # print('!!!', current_word)
            # print('!!!!', tokens)
            if current_word:
                if current_word not in self.tmp[length].keys():
                    self.tmp[length][current_word] = {}
                next_word = tokens[i + 1][-(1 % int(length))]
                # print(current_word, next_word, tokens[i+1], 1%int(length), length)
                if next_word != tokens[i][-1]:
                    if next_word not in self.tmp[length][current_word].keys():
                        self.tmp[length][current_word][next_word] = 0
                    self.tmp[length][current_word][next_word] += 1
                    # print(current_word, next_word, self.tmp[length][current_word])

    '''Возвращает словарь с уже имеющимися данными'''

    def get_data(self):
        out = open('model.json', mode='r')
        self.tmp = dict(json.load(out))

    '''На случай, если нет изначально обученной модели - создаёт каркас в формате JSON'''

    def iternal_start(self):
        initial_data = {
            'books': [],
            1: {},
            2: {},
            3: {},
            4: {},
            5: {}
        }
        file = open('model.json', mode='w')
        json.dump(initial_data, file)
        file.close()

    '''Разбивает полученный файл/текст на токены'''

    def tokenization(self, filename=None, txt=None, n=1):
        if filename:
            file = open(filename, 'rt')
            txt = file.read()
            file.close()
        raw_tokens = list(
            _ for _ in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', txt)) if _.isalpha())
        # print(raw_tokens)
        tokens = list(zip(*[raw_tokens[i:] for i in range(n)]))
        # print('!!!', n, tokens)
        # print(tokens)
        return tokens, raw_tokens


if __name__ == '__main__':
    sample = Ngrams()
    # sample.iternal_start()
    # sample.tokenization(filename='data/Мастер и Маргарита.txt', n=6)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        action='store_const',
        const=True,
        default=False
    )
    parser.add_argument(
        '--input-dir',
        nargs='+',
        type=str,
        required=False,
        help='path to text to fit (default stdin)'
    )

    my_namespace = parser.parse_args()
    # print(sys.argv[1:])
    # print(my_namespace.input_dir)
    if my_namespace.model:
        print('PATH of model: ' + os.path.abspath('model.json'))
    if my_namespace.input_dir:
        # print(my_namespace.input_dir)
        data = ' '.join(my_namespace.input_dir)
        sample.fit(file=data)
        # print('!!', data)
    else:
        text = ''
        for i in sys.stdin.readlines():
            text += i
        sample.fit(text=text)
        # stdin = sys.stdin.readlines()
        # print(stdin)
