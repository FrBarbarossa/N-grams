import pprint
import re
import os
import json
import argparse
import random
import sys


class Ngrams:
    def __init__(self):
        if 'model.json' not in os.listdir():
            self.iternal_start()
        self.tmp = {}

    def generate(self, text=None, length=0):
        self.get_data()
        phrase = self.tokenization(txt=text)[1]
        current_length = len(phrase)
        while current_length < length:
            found = False
            part_length = 5 if current_length >= 5 else current_length
            while part_length >= 1 and not found:
                tail = ' '.join(phrase[-part_length:])
                if tail in self.tmp[str(part_length)].keys():
                    # print(part_length, phrase, list(self.tmp[str(part_length)][tail].items()))
                    variants = sorted(list(self.tmp[str(part_length)][tail].items()), key=lambda x: -x[1])
                    phrase.append(variants[0][0])
                    current_length += 1
                    found = True
                else:
                    part_length -= 1
            else:
                if not found:
                    phrase.append(random.choice(list(self.tmp['1'].keys())))
                    current_length += 1
        print(phrase)

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
            i for i in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', txt)) if i.isalpha())
        tokens = list(zip(*[raw_tokens[i:] for i in range(n)]))
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
        '--prefix',
        nargs='+',
        type=str,
        required=False,
        help='path to text to fit (default stdin)'
    )

    parser.add_argument(
        '--length',
        nargs=1,
        type=int,
        required=True,
        help='length of required phrase'
    )

    my_namespace = parser.parse_args()
    # print(sys.argv[1:])
    # print(my_namespace.input_dir)
    phrase_length = my_namespace.length[0]
    if my_namespace.model:
        print('PATH of model: ' + os.path.abspath('model.json'))
    if my_namespace.prefix:
        text = ' '.join(my_namespace.prefix)
        sample.generate(text=text, length=phrase_length)
        # print(text, phrase_length)
        # sample.fit(file=data)
        # print('!!', data)
    else:
        text = ''
        sample.generate(text=text, length=phrase_length)
        # sample.fit(text=text)
        # stdin = sys.stdin.readlines()
        # print(stdin)
