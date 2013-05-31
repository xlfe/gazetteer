import sys

prev = None
count = 1

for line in sys.stdin.readlines():

    k = line[:-1]

    if k != prev:

        print '{0}\t{1}'.format(prev,count)
        count = 1
        prev = k

    else:
        count += 1


