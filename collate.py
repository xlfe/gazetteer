import sys
import json

prev = None
group = []

#In [6]: d.score.describe()
#Out[6]:
#count    7428244.000000
#mean           3.353387
#std            3.220209
#min            0.219735
#25%            1.734940
#50%            2.633749
#75%            4.018773
#max          158.159691
#dtype: float64

threshold = 2.6
uniqueness = 125000
skipped=0
added = 0

for line in sys.stdin.readlines():
    k,v = line[:-1].split('\t')

    if k != prev:
        #print out the previous group
        if len(group) < uniqueness and len(group) > 0:
            #print '{} {}'.format(len(group),prev)
            print '{0},"{1}"'.format(prev,group)

        #reset the group
        prev = k
        group = []

    nn,score = v.split(',')
    nn = int(nn[1:])
    score = float(score[:-1])

    if score > threshold:
        added +=1
        group.append([nn,score])
    else:
        skipped +=1

#print '{} added'.format(added)
#print '{} skipped'.format(skipped)




