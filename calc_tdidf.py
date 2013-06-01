
import sys
import re
import collections
import math

column = sys.argv[1]

tf = collections.defaultdict(lambda: collections.defaultdict(int))
df = collections.defaultdict(int)
docs = 0


header = sys.stdin.readline().split(',')

assert column in header,'{} not found in input stream'.format(column)

def g(line,column):
    return line.split(',')[header.index(column)]

def ngrams(tokens, MIN_N=3, MAX_N=3):
    n_tokens = len(tokens)
    for i in xrange(n_tokens):
        for j in xrange(i+MIN_N, min(n_tokens, i+MAX_N)+1):
            yield tokens[i:j]



for line in sys.stdin.readlines():
    nn = g(line,'NoticeNumber')
    terms = []
    for w in re.split('\W',g(re.sub('[0-9_]',' ',line),'ending')):
        if len(w) > 2:
            for t in ngrams(w.lower()):
                tf[nn][t] += 1
                terms.append(t)
    for term in set(terms):
        df[term] += 1

total = len(tf)

for nn in tf:

    for term in tf[nn]:
        tfidf = math.log(float(total) / df[term]) * tf[nn][term]
        print '{0}\t[{1},{2}]'.format(term,nn,tfidf)


