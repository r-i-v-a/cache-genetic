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

	print('\n# videos:', numVideos)
	print('# endpoints:', numEndpoints)
	print('# request descriptions:', numRequests)
	print('# caches:', numCaches)
	print('# cache size:', cacheSize)

	line = file.readline().strip().split(' ')
	videoSizes = np.array(list(map(int, line)))

	print('\nvideo sizes:', videoSizes)
