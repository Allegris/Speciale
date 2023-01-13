from bitarray.util import zeros
from shared import get_alphabet, bitvector_rank
import numpy as np

########################################################
# Class for One Hot Encoding
########################################################

class OneHotEncoding:

	def __init__(self, x):
		self.ohe = self.one_hot_encoding(x)
		self.ranks = self.preprocess_ranks(len(x))

	'''
	Returns a dict {letter: bitarray} where the set bits correspond to the places
	where the given letter appear in string x. E.g., for x = "mississippi$", it returns:
	{'$': bitarray('000000000001'),
	 'i': bitarray('010010010010'),
	 'm': bitarray('100000000000'),
	 'p': bitarray('000000001100'),
	 's': bitarray('001101100000')}
	'''
	def one_hot_encoding(self, x):
		# Initiate dict {letter: bitarray}, bitarray is all zeros
		ohe = {letter: zeros(len(x)) for letter in get_alphabet(x)}
		# Set bits corresponding to chars in x
		for i, char in enumerate(x):
			ohe[char][i] = 1
		return ohe

	'''
	Returns a dict {letter: [word_ranks]} where the np arrays contain the rank
	of each word of x (x is split into words of size 32).
	'''
	def preprocess_ranks(self, n):
		word_size = 32
		no_of_words = (n // word_size) + 1
		# Initiate all-zero rank numpy arrays
		ranks = {letter: np.zeros(no_of_words, dtype = np.int32) \
		   for letter in self.ohe.keys()}
		# Iterate over letters
		for letter in self.ohe.keys():
			# Iterate over words
			for i in range(n // word_size):
				# Count set bits in word
				count = self.ohe[letter][i*word_size : (i+1)*word_size].count(1)
				# New word rank: Add count to current word rank
				ranks[letter][i+1] = ranks[letter][i] + count
		return ranks


	'''
	Returns the rank of a given letter, c, and index, i, into string x.
	'''
	def rank(self, c, i):
		# We query for 1's in bitvector for letter c
		return bitvector_rank(self.ohe[c], self.ranks[c], 1, i)

