import bwt_search as bwt_O
import bwt_search_wt as bwt_wt
import wavelet_tree_lvl as lop
from shared import huffman_codes
from shared_bwt import construct_sa_skew, construct_sparse_sa, bwt
from math import floor, log2


x = "AACGTAAACGTAAC"
x += "$"
n = len(x)

sa = construct_sa_skew(x)
sparse_sa = construct_sparse_sa(sa, floor(log2(n)))
num_to_letter_dict, letter_to_num_dict, num_ls = bwt_O.map_string_to_ints(x)

# BW search with Occ table
C = bwt_O.construct_C(x)
O = bwt_O.construct_O(x, sa, num_to_letter_dict)

# BW search with wavelet tree rank query (level order wt)
bwt_x = bwt(x, sa)
C_dict = bwt_wt.construct_C(x)
codes = huffman_codes(x)

# BW search with wavelet tree rank query (level order wt with pointers)
codes2 = huffman_codes(bwt_x)
wt2, pointers = lop.wavelet_tree(bwt_x, codes2)
ranks2 = lop.all_node_ranks(wt2, len(bwt_x), pointers)

def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n, sparse_sa, C_dict, wt2, pointers, ranks2, codes2) == ls

