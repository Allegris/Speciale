'''
Returns a lex sorted list of the letters of x
'''
def get_alphabet(x):
	letters = ''.join(set(x))
	return sorted(letters)