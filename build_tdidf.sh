#!/bin/bash

#cat ./data/employments.csv | python tokens.py | sort | uniq -c >| tf_all.txt
cat ./data/employments.csv | python calc_tdidf.py ending
