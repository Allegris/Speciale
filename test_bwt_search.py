import bwt_search as bwt_O
import bwt_search_wt as bwt_wt
import wavelet_tree_lvl as lop
from shared import huffman_codes
from shared_bwt import construct_sa_skew, construct_sparse_sa, bwt
from math import floor, log2


x = "AACGTAAACGTAAC$"
n = len(x)
sa = construct_sa_skew(x)
sparse_sa = construct_sparse_sa(sa, floor(log2(n)))
bwt_x = bwt(x, sa)

# BW search with O table
num_to_letter_dict, letter_to_num_dict, _ = bwt_O.map_string_to_ints(x)
C = bwt_O.construct_C(x)
O = bwt_O.construct_O(x, sa, num_to_letter_dict)

# BW search with wavelet tree rank query (level order wt)
SENTINEL_idx = bwt_x.index("$")
C_dict = bwt_wt.construct_C(x)
x2 = x[:-1] # remove sentinel from x
n2 = len(x2)
bwt_x2 = bwt_x.replace("$", "") # remove sentinel from bwt(x)
codes = huffman_codes(x2)
wt, pointers = lop.wavelet_tree(bwt_x2, codes)
ranks = lop.all_node_ranks(wt, len(bwt_x2), pointers)

def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls

def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict) == ls
	assert bwt_wt.bw_search(bwt_x, p, n2, sparse_sa, C_dict, wt, pointers, ranks, codes, SENTINEL_idx) == ls



mis = "mississippi$"
n_mis = len(mis)
sa_mis = construct_sa_skew(mis)
sparse_sa_mis = construct_sparse_sa(sa_mis, 4)
bwt_mis = bwt(mis, sa_mis)

# BW search with O table
num_to_letter_dict_mis, letter_to_num_dict_mis, _ = bwt_O.map_string_to_ints(mis)
C_mis = bwt_O.construct_C(mis)
O_mis = bwt_O.construct_O(mis, sa_mis, num_to_letter_dict_mis)

# BW search with wavelet tree rank query (level order wt)
SENTINEL_idx_mis = bwt_mis.index("$")
C_dict_mis = bwt_wt.construct_C(mis)
mis2 = mis[:-1] # remove sentinel from x
n2_mis = len(x2)
bwt_mis2 = bwt_mis.replace("$", "") # remove sentinel from bwt(x)
codes_mis = huffman_codes(mis2)
wt_mis, pointers_mis = lop.wavelet_tree(bwt_mis2, codes_mis)
ranks_mis = lop.all_node_ranks(wt_mis, len(bwt_mis2), pointers_mis)


def test_mississippi_m():
	p = "m"
	ls = [0]
	assert bwt_O.bw_search(bwt_mis, p, sparse_sa_mis, C_mis, O_mis, letter_to_num_dict_mis) == ls
	assert bwt_wt.bw_search(bwt_mis, p, n2_mis, sparse_sa_mis, C_dict_mis, wt_mis, pointers_mis, ranks_mis, codes_mis, SENTINEL_idx_mis) == ls

def test_mississippi_iss():
	p = "iss"
	ls = [1, 4]
	assert bwt_O.bw_search(bwt_mis, p, sparse_sa_mis, C_mis, O_mis, letter_to_num_dict_mis) == ls
	assert bwt_wt.bw_search(bwt_mis, p, n2_mis, sparse_sa_mis, C_dict_mis, wt_mis, pointers_mis, ranks_mis, codes_mis, SENTINEL_idx_mis) == ls

def test_mississippi_ssi():
	p = "ssi"
	ls = [2, 5]
	assert bwt_O.bw_search(bwt_mis, p, sparse_sa_mis, C_mis, O_mis, letter_to_num_dict_mis) == ls
	assert bwt_wt.bw_search(bwt_mis, p, n2_mis, sparse_sa_mis, C_dict_mis, wt_mis, pointers_mis, ranks_mis, codes_mis, SENTINEL_idx_mis) == ls
















