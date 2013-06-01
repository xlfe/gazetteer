
import sys
import re
from nltk.stem.wordnet import WordNetLemmatizer

header = sys.stdin.readline().split(',')

lmtzr = WordNetLemmatizer()


def g(line,column):
    return line.split(',')[header.index(column)]


for line in sys.stdin.readlines():
    nn = g(line,'NoticeNumber')
    for w in re.split('\W',g(re.sub('[0-9_]',' ',line),'ending')):
        if len(w) > 2:
            print '{1}'.format(nn,w)
            #print '{1}\t{0}'.format(nn,stem)
