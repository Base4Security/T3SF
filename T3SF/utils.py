from difflib import SequenceMatcher
from collections import Counter
import os

process_wait = False
process_quit = False
process_started = False

def is_docker():
	"""
	Detects if the script is running inside a docker environment.
	"""
	path = '/proc/self/cgroup'
	return (
		os.path.exists('/.dockerenv') or
		os.path.isfile(path) and any('docker' in line for line in open(path))
	)

def similar(a, b):
	"""
	Based in graphics, find the similarity between 2 strings.
	"""
	return SequenceMatcher(None, a, b).ratio()

def regex_finder(input):
	"""
	Matches repeated words counting the 
	amount of times the word is being repeated.
	"""
	words = input.split('-')
	dict = Counter(words)
	for key in words:
		if dict[key]>1:
			return key
	return False