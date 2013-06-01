import sys
import json

prev = None
group = []

#In [6]: d.score.describe()
#Out[6]:
#count    28719099.000000
#mean            1.859272
#std             2.212058
#min             0.003201
#25%             0.773457
#50%             1.358657
#75%             2.232349
#max           221.910415
#dtype: float64

threshold = 2
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




