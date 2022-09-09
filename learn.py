import numpy as np
import re
import json
import pprint

# # load text
# filename = 'data/Мастер и Маргарита.txt'
# file = open(filename, 'rt')
# text = file.read()
# file.close()
# # split based on words only
text = 'Алиса, я тебя очень сильно люблю'
# words = list(map(lambda i: i.lower(), re.split(r'\W+', text))
# words = list(
#     _ for _ in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', text)) if _.isalpha())
# print(words)
# tokens = list(zip(*[words[i:] for i in range(3)]))
# print(tokens)
n=2
raw_tokens = list(
    _ for _ in map(lambda i: i.lower() if i.isalpha() else '', re.split(r'\W+', text)) if _.isalpha())
tokens = list(zip(*[raw_tokens[i:] for i in range(n)]))
print(tokens)

# ones = {}
# with open("model.json", "w") as write_file:
#     # json.dump(data, write_file)
#     for i in range(len(words)-1):
#         current_word = words[i]
#         if current_word:
#             if current_word not in ones.keys():
#                 ones[current_word] = {}
#             next_word = words[i+1]
#             if next_word not in ones[current_word].keys():
#                 ones[current_word][next_word] = 0
#             ones[current_word][next_word] += 1
#     json.dump(ones, write_file)
#
# a=list(ones['в'].items())
# a.sort(key = lambda x: -x[1])
# print(a)
# print(len(ones.keys()))
# print(words[:100])

# out = open('model.json', mode='r')
# # pprint.pprint(sorted(dict(json.load(out))['2']['люблю тебя'].items(), key=lambda x: -x[-1]))
# pprint.pprint(dict(json.load(out))['3']['и я очень'])
a = [1,3,4]
print(abs(-1)%1)
print(a[- abs(-1)%3])