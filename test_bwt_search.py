import bwt_search as bw
import wavelet_tree_level_order as lo


x = "AACGTAAACGTAAC"
x += "$"

sa = bw.construct_sa_skew(x)
num_to_letter_dict, letter_to_num_dict, num_ls = bw.map_string_to_ints(x)

# BW search with Occ table
C = bw.construct_C(x)
O = bw.construct_O(x, sa, num_to_letter_dict)

# BW search with wavelet tree rank query (level order wt)
bwt_x = bw.bwt(x, sa)
select = bw.construct_select_dict(x)
wt, codes = lo.wavelet_tree(bwt_x)
ranks = lo.preprocess_node_ranks(wt, len(bwt_x))


def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert bw.bw_search(x, sa, p, C, O, letter_to_num_dict) == ls
	assert bw.bw_seach_rank(bwt_x, sa, p, select, wt, ranks, codes) == ls

