
import sys
import re

header = sys.stdin.readline().split(',')

def g(line,column):
    return line.split(',')[header.index(column)]

def ngrams(tokens, MIN_N=3, MAX_N=3):
    n_tokens = len(tokens)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            yield tokens[i:j]


for line in sys.stdin.readlines():
    terms = []
    for w in re.split('\W',g(re.sub('[0-9_]',' ',line),'ending')):
        if len(w) > 2:

            for t in ngrams(w.lower()):
                terms.append(t)
            for t in set(terms):
                print t
