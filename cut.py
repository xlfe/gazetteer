import sys

for line in sys.stdin.readlines():
    k,v = line[:-1].split('\t')
    nn,tdidf = v.split(',')

    print '{},{},{}'.format(k,nn[1:],tdidf[:-1])