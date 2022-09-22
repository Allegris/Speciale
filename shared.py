

'''
Returns a lex sorted list of the letters of x
'''
def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)

def alphabet_size(x):
	letters = ''.join(set(x))
	return len(letters)

def letter_count(x):
	alpha = get_alphabet(x)
	# Map between letters and ints
	counts = {a: 0 for a in alpha}
	for char in x:
		counts[char] += 1
	return counts