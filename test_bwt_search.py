import bwt_search as bw
import bwt_search_wt as bwt_wt
import wavelet_tree_level_order as lo
import wavelet_tree_level_order_pointers as lop


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
wt, codes = lo.wavelet_tree_and_codes(bwt_x)
ranks = lo.preprocess_tree_node_ranks(wt, len(bwt_x))

# BW search with wavelet tree rank query (level order wt with pointers)
wt2, pointers, codes2 = lop.wavelet_tree_and_child_dict_and_codes(bwt_x)
ranks2 = lop.preprocess_tree_node_ranks(wt2, len(bwt_x), pointers)

def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert bw.bw_search(p, sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(p, n, sa, C_dict, wt, ranks, codes) == ls
	assert bwt_wt.bw_search2(p, n, sa, C_dict, wt2, pointers, ranks2, codes2) == ls

