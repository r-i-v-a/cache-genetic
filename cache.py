#!/usr/bin/env python

import numpy as np
import random
import sys

INPUT_FILE = '../data/me_at_the_zoo.in'
ITERATIONS = 2
POPULATION = []
POPULATION_SIZE = 10
SCORES = []

def readLineAsNumbers(file):
	return list(map(int, file.readline().strip().split(' ')))

def readTimeSaved(file, numEndpoints):
	timeSaved = []

	for i in range(numEndpoints):
		line = readLineAsNumbers(file)
		dataCenterLatency = line[0]
		numConnectedCaches = line[1]
		endpointCaches = []

		for j in range(numConnectedCaches):
			line = readLineAsNumbers(file)
			endpointCaches.append((line[0], dataCenterLatency - line[1]))

		endpointCaches = sorted(endpointCaches, key=lambda x: x[1], reverse=True)
		timeSaved.append(endpointCaches)

	return timeSaved

def readRequests(file, numRequests):
	requests = []

	for i in range(numRequests):
		line = readLineAsNumbers(file)
		requests.append((line[0], line[1], line[2]))

	return requests

def isOverCapacity(cache, videoSizes, cacheSize):
	used = sum(map(lambda x: videoSizes[x], cache))
	return used > cacheSize

def evaluateSolution(solution, requests, videoSizes, cacheSize, timeSaved):
	score = 0
	totalRequests = 0

	for i in range(len(requests)):
		totalRequests += requests[i][2]
		for cache in timeSaved[requests[i][1]]:
			if (requests[i][0] in solution['caches'][cache[0]]):
				score += cache[1] * requests[i][2]
				break

	return (score * 1000) // totalRequests

def startPopulation(numCaches, numVideos):
	for i in range(POPULATION_SIZE):
		solution = {}
		solution['caches'] = []
		solution['score'] = 0

		for j in range(numCaches):
			solution['caches'].append(set())

		POPULATION.append(solution)

def mutateCache(cache, numVideos, videoSizes, cacheSize):
	cache.add(random.randrange(numVideos))

	while (isOverCapacity(cache, videoSizes, cacheSize)):
		x = random.sample(cache, 1)
		cache.discard(x[0])

def mutatePopulation(numVideos, videoSizes, cacheSize):
	for solution in POPULATION:
		for cache in solution['caches']:
			mutateCache(cache, numVideos, videoSizes, cacheSize)

with open(INPUT_FILE, 'r') as file:
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

	videoSizes = readLineAsNumbers(file)
	print('\nvideo sizes:', videoSizes)

	timeSaved = readTimeSaved(file, numEndpoints)
	print('\ncache latencies:', timeSaved)

	requests = readRequests(file, numRequests)
	print('\nrequests:', requests)

startPopulation(numCaches, numVideos)

for i in range(ITERATIONS):
	mutatePopulation(numVideos, videoSizes, cacheSize)

	for solution in POPULATION:
		solution['score'] = evaluateSolution(solution, requests, videoSizes, cacheSize, timeSaved)

	POPULATION = sorted(POPULATION, key=lambda x: x['score'], reverse=True)
	SCORES.append((i, POPULATION[0]['score']))

	print('\niteration:', i)
	print('population:', POPULATION)

print('\nsummary:', SCORES)