import sys

prev = None
group = []

for line in sys.stdin.readlines():
    k,v = line[:-1].split('\t')

    if k != prev:
        #print out the previous group
        if len(group) > 0:
            print '{0}\t{1}'.format(prev,group)

        #reset the group
        group = []

        prev = k
    else:
        group.append(v)

