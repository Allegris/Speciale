from pprint import pprint
import bwt_search_wt as bw
from bitarray.util import canonical_huffman
from shared import get_alphabet


def letter_count(x):
	alpha = get_alphabet(x)
	# Map between letters and ints
	counts = {a: 0 for a in alpha}
	for char in x:
		counts[char] += 1
	return counts



x =  "mississippi"

cnt = letter_count(x)


codedict, count, symbol = canonical_huffman(cnt)

pprint(codedict)
