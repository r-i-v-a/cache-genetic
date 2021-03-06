#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import random
import sys

INPUT_FILE = '../data/me_at_the_zoo.in'

ITERATIONS = 1000
POPULATION_SIZE = 100
KEEP = 10
DISCARD = 25

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
	return sum(map(lambda x: videoSizes[x], cache)) > cacheSize

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

# make a deep copy of a cache
def deepCopy(cache):
	copy = set()
	for video in cache:
		copy.add(video)
	return copy

# apply mutations (incremental additions / swaps)
def mutateCache(cache, numVideos, videoSizes, cacheSize):
	cache.add(random.randrange(numVideos))

	while (isOverCapacity(cache, videoSizes, cacheSize)):
		x = random.sample(cache, 1)
		cache.discard(x[0])

# choose random combination of caches from 2 parents
def crossoverSolutions(a, b, numCaches):
	offspring = {}
	offspring['caches'] = []
	offspring['score'] = 0

	for i in range(numCaches):
		offspring['caches'].append(deepCopy((a, b)[random.randrange(2)]['caches'][i]))

	return offspring

# next -- keep best, discard worst, recombine to create others
def makeNextGeneration(numVideos, videoSizes, numCaches, cacheSize):
	next = []

	for i in range(KEEP):
		next.append(POPULATION[i])

	for i in range(KEEP, POPULATION_SIZE):
		a = random.randrange(POPULATION_SIZE - DISCARD)
		b = random.randrange(POPULATION_SIZE - DISCARD)
		offspring = crossoverSolutions(POPULATION[a], POPULATION[b], numCaches)
		for cache in offspring['caches']:
			mutateCache(cache, numVideos, videoSizes, cacheSize)
		next.append(offspring)

	return next

# print all members of current population
def printPopulation():
	for solution in POPULATION:
		print('\nscore:', solution['score'])
		print('caches:', solution['caches'])

# plot best score attained x generation
def plotScores():
	plt.plot(BEST)
	plt.xlabel('generation')
	plt.ylabel('best score')
	plt.show()

# read input
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

# run genetic algorithm
startPopulation(numCaches, numVideos)
print('\ntraining:')

for i in range(ITERATIONS):
	POPULATION = makeNextGeneration(numVideos, videoSizes, numCaches, cacheSize)

	for solution in POPULATION:
		solution['score'] = evaluateSolution(solution, requests, videoSizes, cacheSize, timeSaved)

	POPULATION = sorted(POPULATION, key=lambda x: x['score'], reverse=True)
	BEST.append(POPULATION[0]['score'])
	print(i, '--', POPULATION[0]['score'])

printPopulation()
plotScores()