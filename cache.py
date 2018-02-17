#!/usr/bin/env python

import numpy as np
import sys

def readLineAsNumbers(file):
	return list(map(int, file.readline().strip().split(' ')))

with open('../data/me_at_the_zoo.in', 'r') as file:
	line = readLineAsNumbers(file)

	numVideos = line[0]
	numEndpoints = line[1]
	numRequests = line[2]
	numCaches = line[3]
	cacheSize = line[4]

	print('\n# videos:', numVideos)
	print('# endpoints:', numEndpoints)
	print('# request descriptions:', numRequests)
	print('# caches:', numCaches)
	print('# cache size:', cacheSize)

	videoSizes = np.array(readLineAsNumbers(file))

	print('\nvideo sizes:', videoSizes)

	cacheLatency = []

	for i in range(numEndpoints):
		line = readLineAsNumbers(file)
		dataCenterLatency = line[0]
		numConnectedCaches = line[1]
		endpointCaches = []

		for j in range(numConnectedCaches):
			line = readLineAsNumbers(file)
			endpointCaches.append((line[0], dataCenterLatency - line[1]))

		endpointCaches = sorted(endpointCaches, key=lambda x: x[1], reverse=True)
		cacheLatency.append(endpointCaches)

		print('\nendpoint:', i)
		print('connected caches:', endpointCaches)
