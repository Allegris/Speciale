import bwt_search as bw
import bwt_search_wt as bwt_wt
import wavelet_tree_lvl as lop
from shared import huffman_codes


x = "AACGTAAACGTAAC"
x += "$"
n = len(x)

sa = bw.construct_sa_skew(x)
num_to_letter_dict, letter_to_num_dict, num_ls = bw.map_string_to_ints(x)

# BW search with Occ table
C = bw.construct_C(x)
O = bw.construct_O(x, sa, num_to_letter_dict)

# BW search with wavelet tree rank query (level order wt)
bwt_x = bwt_wt.bwt(x, sa)
C_dict = bwt_wt.construct_C_dict(x)
codes = huffman_codes(x)

# BW search with wavelet tree rank query (level order wt with pointers)
codes2 = huffman_codes(bwt_x)
wt2, pointers = lop.wavelet_tree(bwt_x, codes2)
ranks2 = lop.all_node_ranks(wt2, len(bwt_x), pointers)

def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

