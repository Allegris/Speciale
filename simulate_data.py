from numpy.random import choice
from shared import get_alphabet


# DNA alphabet: size 4
alpha = ["A", "C", "G", "T"]
probs = [0.25] * len(alpha)


'''
# Big alphabet: size 50
x = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ"
alpha = get_alphabet(x) # size 50
probs = [1 / len(alpha)] * len(alpha) # equal probs
'''

def generate_string(n):
	return "".join(choice(alpha, n, p=probs))


def print_to_file(n):
	title = f"simulated_data\\simulated_Big_n{n}.txt"
	file = open(title, "w")
	file.write(generate_string(n))
	file.close()


##########################################################################
# Code to run
##########################################################################


#ns = list(range(1000, 10001, 1000)) # 1K
ns = list(range(1000, 10001, 1000)) #  10K
#ns = list(range(10000, 100001, 10000)) # 100K
#ns = list(range(50000, 1000001, 50000)) # 1M

for n in ns:
	print_to_file(n)










