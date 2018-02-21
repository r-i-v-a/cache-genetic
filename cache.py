#!/usr/bin/env python

import numpy as np
import random
import sys

INPUT_FILE = '../data/me_at_the_zoo.in'

ITERATIONS = 100
POPULATION_SIZE = 100

POPULATION = []
BEST = []

# parse input line
def readLineAsNumbers(file):
	return list(map(int, file.readline().strip().split(' ')))

# parse input -- time saved for some endpoint, cache
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

# parse input -- request descriptions
def readRequests(file, numRequests):
	requests = []

	for i in range(numRequests):
		line = readLineAsNumbers(file)
		requests.append((line[0], line[1], line[2]))

	return requests

# test if video set exceeds cache capacity
def isOverCapacity(cache, videoSizes, cacheSize):
	used = sum(map(lambda x: videoSizes[x], cache))
	return used > cacheSize

# score for candidate solution: average time saved
def evaluateSolution(solution, requests, videoSizes, cacheSize, timeSaved):
	score = 0
	totalRequests = 0

	for request in requests:
		totalRequests += request[2]
		for cache in timeSaved[request[1]]:
			if (request[0] in solution['caches'][cache[0]]):
				score += cache[1] * request[2]
				break

	return (score * 1000) // totalRequests

# initialize population -- empty caches
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

def crossoverSolutions(a, b, numCaches):
	offspring = {}
	offspring['caches'] = []
	offspring['score'] = 0

	for i in range(numCaches):
		parents = (a, b)
		offspring['caches'].append(parents[random.randrange(2)]['caches'][i])

	print('\nparent 1:', a)
	print('parent 2:', b)
	print('offspring:', offspring)

	return offspring

def makeNextGeneration(numVideos, videoSizes, numCaches, cacheSize):
	next = []

	for i in range(POPULATION_SIZE):
		a = random.randrange(POPULATION_SIZE // 2)
		b = random.randrange(POPULATION_SIZE // 2)
		next.append(crossoverSolutions(POPULATION[a], POPULATION[b], numCaches))

	for solution in next:
		for cache in solution['caches']:
			mutateCache(cache, numVideos, videoSizes, cacheSize)

	return next

def printPopulation():
	for solution in POPULATION:
		print('\nscore:', solution['score'])
		print('caches:', solution['caches'])

def printSummary():
	print('\nsummary:')
	for entry in BEST:
		print(entry[0], ' -- ', entry[1]['score'])

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
	POPULATION = makeNextGeneration(numVideos, videoSizes, numCaches, cacheSize)

	for solution in POPULATION:
		solution['score'] = evaluateSolution(solution, requests, videoSizes, cacheSize, timeSaved)

	POPULATION = sorted(POPULATION, key=lambda x: x['score'], reverse=True)
	BEST.append((i, POPULATION[0]))

	print('\niteration:', i)
	printPopulation()

printSummary()