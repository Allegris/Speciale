from bitarray import bitarray

'''
                    111111111122
          0123456789012345678901
bitarray('0011011011010000111100')

bitarray('00110110110')
bitarray('10000')
bitarray('111100')

'''


def rank(wt, n, c, i):
	root = wt[0:n]
	print(root)
	print(go_left(root, n, 0, n))
	print(go_right(root, n, 0, n))


def go_left(sub_bv, n, i, j):
	return i+n, i+n+sub_bv.count(0)

def go_right(sub_bv, n, i, j):
	return i+n+sub_bv.count(0), i+n+sub_bv.count(0)+sub_bv.count(1)

#bv = bitarray('0011011011010000111100')
#sub_bv = bv[0:11]
#print(go_left(sub_bv, len(bv), 0, len(sub_bv)))

x = "mississippi"
n = len(x)
wt = bitarray('0011011011010000111100')

rank(wt, n, "i", 8)






