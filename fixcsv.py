import sys
import re

header = sys.stdin.readline()[:-1].split(',')

header.append('date_gazetted')

print ','.join(h for h in header)


for line in sys.stdin.readlines():

    cells = line[:-1].split(',')

    try:
        cells[0] = re.match(r'[^0-9]*([0-9]+[\ ]*[0-9]+)',cells[0]).group(1).replace(' ','')
    except AttributeError:
        cells[0] = '0'

    cells.append(cells[3][5:])

    print ','.join(c for c in cells)