import bwt_search as bwt_O
import bwt_search_wt_lvl as bwt_wt_lvl
import bwt_search_wt as bwt_wt
from wavelet_tree_lvl import wavelet_tree
from wavelet_tree import WaveletTreeNode
from shared import construct_sa_skew, construct_sparse_sa, bwt
from math import floor, log2

'''
# BWT example:
x: AACGTAAACGTAAC$

$AACGTAAACGTAAC  0
AAACGTAAC$AACGT  1
AAC$AACGTAAACGT  2
AACGTAAACGTAAC$  3
AACGTAAC$AACGTA  4
AC$AACGTAAACGTA  5
ACGTAAACGTAAC$A  6
ACGTAAC$AACGTAA  7
C$AACGTAAACGTAA  8
CGTAAACGTAAC$AA  9
CGTAAC$AACGTAAA  10
GTAAACGTAAC$AAC  11
GTAAC$AACGTAAAC  12
TAAACGTAAC$AACG  13
TAAC$AACGTAAACG  14

btw(x) = CTT$AAAAAAACCGG
'''

x = "AACGTAAACGTAAC$"
sa = construct_sa_skew(x)
sparse_sa = construct_sparse_sa(sa, floor(log2(len(x))))
bwt_x = bwt(x, sa)

# BW search with O table
num_to_letter_dict, letter_to_num_dict, _ = bwt_O.map_string_to_ints(x)
C = bwt_O.construct_C(x)
O = bwt_O.construct_O(x, sa, num_to_letter_dict)

# BW search with wavelet tree rank query (level order wt)
SENTINEL_idx = bwt_x.index("$")
C_dict = bwt_wt_lvl.construct_C(x)
# Remove sentinel from bwt(x) before constructing WT
wt = wavelet_tree(bwt_x.replace("$", ""))

wt_root = WaveletTreeNode(bwt_x.replace("$", ""), 0, None)


def O_hits_AACGTAAACGTAAC(p):
	return bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict)

def wt_lvl_hits_AACGTAAACGTAAC(p):
	return bwt_wt_lvl.bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C_dict, wt)

def wt_hits_AACGTAAACGTAAC(p):
	return bwt_wt.bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C_dict, wt_root)


def test_AACGTAAACGTAAC_AAC():
	p = "AAC"
	ls = [0, 6, 11]
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)


def test_AACGTAAACGTAAC_ACC():
	p = "ACC"
	ls = []
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)

def test_AACGTAAACGTAAC_AA():
	p = "AA"
	ls = [0, 5, 6, 11]
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)

def test_AACGTAAACGTAAC_A():
	p = "A"
	ls = [0, 1, 5, 6, 7, 11, 12]
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)

def test_AACGTAAACGTAAC_AACGTAAACGTAACA():
	p = "AACGTAAACGTAACA"
	ls = []
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)

def test_AACGTAAACGTAAC_C():
	p = "C"
	ls = [2, 8, 13]
	assert ls == O_hits_AACGTAAACGTAAC(p)
	assert ls == wt_lvl_hits_AACGTAAACGTAAC(p)
	assert ls == wt_hits_AACGTAAACGTAAC(p)


###############################################################################

mis = "mississippi$"
sa_mis = construct_sa_skew(mis)
sparse_sa_mis = construct_sparse_sa(sa_mis, floor(log2(len(mis))))
bwt_mis = bwt(mis, sa_mis)

# BW search with O table
num_to_letter_dict_mis, letter_to_num_dict_mis, _ = bwt_O.map_string_to_ints(mis)
C_mis = bwt_O.construct_C(mis)
O_mis = bwt_O.construct_O(mis, sa_mis, num_to_letter_dict_mis)

# BW search with wavelet tree rank query (level order wt)
SENTINEL_idx_mis = bwt_mis.index("$")
C_dict_mis = bwt_wt_lvl.construct_C(mis)
# Remove sentinel from bwt(x) before constructing WT
wt_mis = wavelet_tree(bwt_mis.replace("$", ""))

wt_root_mis = WaveletTreeNode(bwt_mis.replace("$", ""), 0, None)

def O_hits_mississippi(p):
	return bwt_O.bw_search(bwt_mis, p, sparse_sa_mis, C_mis, O_mis, letter_to_num_dict_mis)

def wt_lvl_hits_mississippi(p):
	return bwt_wt_lvl.bw_search(p, bwt_mis, SENTINEL_idx_mis, sparse_sa_mis, C_dict_mis, wt_mis)

def wt_hits_mississippi(p):
	return bwt_wt.bw_search(p, bwt_mis, SENTINEL_idx_mis, sparse_sa_mis, C_dict_mis, wt_root_mis)



def test_mississippi_m():
	p = "m"
	ls = [0]
	assert ls == O_hits_mississippi(p)
	assert ls == wt_lvl_hits_mississippi(p)
	assert ls == wt_hits_mississippi(p)

def test_mississippi_iss():
	p = "iss"
	ls = [1, 4]
	assert ls == O_hits_mississippi(p)
	assert ls == wt_lvl_hits_mississippi(p)
	assert ls == wt_hits_mississippi(p)

def test_mississippi_ssi():
	p = "ssi"
	ls = [2, 5]
	assert ls == O_hits_mississippi(p)
	assert ls == wt_lvl_hits_mississippi(p)
	assert ls == wt_hits_mississippi(p)















