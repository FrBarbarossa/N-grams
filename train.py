import re
import os
import json
import argparse
import sys


class Ngrams:
    def __init__(self):
        if 'model.json' not in os.listdir():
            self.__iternal_start()
        self.tmp = {}

    def fit(self, text=None, file=None):
        self.get_data()
        if file:
            files = [i for i in os.listdir(file)]
            for path in files:
                print("Читаю книгу:..", path)
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

            self.update_data(tokens=tokens[0], length=str(token_length))

    def update_data(self, tokens, length):
        for i in range(len(tokens) - 1):
            current_word = ' '.join(tokens[i])
            if current_word:
                next_word = tokens[i + 1][-(1 % int(length))]
                if next_word != tokens[i][-1]:
                    if current_word not in self.tmp[length].keys():
                        self.tmp[length][current_word] = {}
                    if next_word not in self.tmp[length][current_word].keys():
                        self.tmp[length][current_word][next_word] = 0
                    self.tmp[length][current_word][next_word] += 1

    def get_data(self):
        out = open('model.json', mode='r')
        self.tmp = dict(json.load(out))

    def __iternal_start(self):
        initial_data = {
            1: {},
            2: {},
            3: {},
            4: {},
            5: {}
        }
        file = open('model.json', mode='w')
        json.dump(initial_data, file)
        file.close()

    def tokenization(self, filename=None, txt=None, n=1):
        if filename:
            file = open(filename, 'rt')
            txt = file.read()
            file.close()
        raw_tokens = list(
            _ for _ in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', txt)) if _.isalpha())
        tokens = list(zip(*[raw_tokens[i:] for i in range(n)]))
        return tokens, raw_tokens


if __name__ == '__main__':
    sample = Ngrams()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--model',
        action='store_const',
        const=True,
        default=False,
        help='To explore path to model'
    )
    parser.add_argument(
        '--input-dir',
        nargs='+',
        type=str,
        required=False,
        help='Use --input-dir PATH/FILE to enter directory where you put .txt files to train model. \n If you doesn`t use --input-dir, you may enter text in console (stdin)'
    )

    my_namespace = parser.parse_args()
    if my_namespace.model:
        print('PATH of model: ' + os.path.abspath('model.json'))
    if my_namespace.input_dir:
        data = ' '.join(my_namespace.input_dir)
        sample.fit(file=data)
    else:
        text = ''
        print("Введите текст ниже: ")
        for i in sys.stdin.readlines():
            text += i
        sample.fit(text=text)
