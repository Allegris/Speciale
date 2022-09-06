from bitarray import bitarray
from math import log2, floor
import wavelet_shared as wts

class WaveletTreeNode:
	def __init__(self, x, root):
		self.x = x
		self.n = len(x)
		self.alpha = wts.get_alphabet(x)
		self.bitvector = None
		self.ranks = None
		self.left_child = None
		self.right_child = None

		# If node has no root: it IS root
		if not root:
			self.root = self
			self.codes = {letter: bitarray() for letter in self.alpha}
		else:
			self.root = root

		# Split alphabet to create children
		bv, left, right = wts.split_node(self, x)
		if bv:
			print("case node", x)
			self.bitvector = bv
			self.left_child = WaveletTreeNode(left, self)
			self.right_child = WaveletTreeNode(right, self)
		else:
			print("case leaf", x)
			self.left_child = WaveletTreeLeaf(left)
			self.right_child = WaveletTreeLeaf(right)



class WaveletTreeLeaf:
	def __init__(self, letter):
		self.letter = letter


x = "mississippi"
wt = WaveletTreeNode(x, False)
print("TEST", wt.left_child.left_child.left_child.letter)


