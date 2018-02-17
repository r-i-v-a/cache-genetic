#!/usr/bin/env python

import numpy as np
import sys

with open('../data/kittens.in', 'r') as file:
	line = file.readline().strip().split(' ')

	numVideos = int(line[0])
	numEndpoints = int(line[1])
	numRequests = int(line[2])
	numCaches = int(line[3])
	cacheSize = int(line[4])

	print(numVideos, numEndpoints, numRequests, numCaches, cacheSize)
