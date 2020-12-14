import sys
from myjson.convertor import parse
import cProfile

filename = 'sample.json'
with open(filename) as fp:
    contents = fp.read()
    cProfile.runctx('parse(contents)',globals(), locals(), filename='stats')

