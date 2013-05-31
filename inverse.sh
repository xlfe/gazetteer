#!/bin/bash

cat ./data/employments.csv | python inverse.py | sort | python collate.py > sorted.txt
