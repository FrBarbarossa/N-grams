import re
import os
import json
import argparse
import random
import sys


class Ngrams:
    def __init__(self):
        self.tmp = {}

    def generate(self, text=None, length=0):
        self.get_data()
        if not text:
            text = random.choice(list(self.tmp['4'].keys()))
        phrase = self.tokenization(txt=text)[1]
        current_length = len(phrase)
        while current_length < length:
            found = False
            part_length = random.choice([2, 3, 4, 5]) if current_length >= 5 else random.choice(
                range(1, current_length + 1))
            while part_length >= 1 and not found:
                tail = ' '.join(phrase[-part_length:])
                if tail in self.tmp[str(part_length)].keys():
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
        print(' '.join(phrase))

    def get_data(self):
        out = open('model.json', mode='r')
        self.tmp = dict(json.load(out))

    def tokenization(self, filename=None, txt=None, n=1):
        if filename:
            file = open(filename, 'rt')
            txt = file.read()
            file.close()
        raw_tokens = list(
            i for i in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', txt)) if i.isalpha())
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
        '--prefix',
        nargs='+',
        type=str,
        required=False,
        help='Enter the start of phrase (uses as a seed)'
    )

    parser.add_argument(
        '--length',
        nargs=1,
        type=int,
        required=True,
        help='length of required phrase'
    )

    my_namespace = parser.parse_args()
    phrase_length = my_namespace.length[0]
    if my_namespace.model:
        print('PATH of model: ' + os.path.abspath('model.json'))
    if my_namespace.prefix:
        text = ' '.join(my_namespace.prefix)
        sample.generate(text=text, length=phrase_length)
    else:
        text = ''
        sample.generate(text=text, length=phrase_length)
