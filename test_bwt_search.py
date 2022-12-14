import bwt_search as bwt_O
import bwt_search_wt as bwt_wt
import wavelet_tree as wt1
import wavelet_tree_lvl as wt2
from shared import construct_sa_skew, construct_sparse_sa, bwt
from math import floor, log2


x = "AACGTAAACGTAAC$"
sa = construct_sa_skew(x)
sparse_sa = construct_sparse_sa(sa, floor(log2(len(x))))
bwt_x = bwt(x, sa)


##### BW search with O table #####
num_to_letter_dict, letter_to_num_dict, _ = bwt_O.map_string_to_ints(x)
C = bwt_O.construct_C(x)
O = bwt_O.construct_O(x, sa, num_to_letter_dict)


##### BW search with wavelet tree rank query #####
SENTINEL_idx = bwt_x.index("$")
C_dict = bwt_wt.construct_C(x)

# WT Node tree
w1 = wt1.WaveletTree(bwt_x.replace("$", "")) # remove sentinel
# WT level order
w2 = wt2.WaveletTree(bwt_x.replace("$", "")) # remove sentinel



def O_hits_AACGTAAACGTAAC(p):
	return bwt_O.bw_search(bwt_x, p, sparse_sa, C, O, letter_to_num_dict)

def wt_hits_AACGTAAACGTAAC(p):
	return bwt_wt.bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C_dict, w1)

def wt_lvl_hits_AACGTAAACGTAAC(p):
	return bwt_wt.bw_search(p, bwt_x, SENTINEL_idx, sparse_sa, C_dict, w2)



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

##### BW search with O table #####
num_to_letter_dict_mis, letter_to_num_dict_mis, _ = bwt_O.map_string_to_ints(mis)
C_mis = bwt_O.construct_C(mis)
O_mis = bwt_O.construct_O(mis, sa_mis, num_to_letter_dict_mis)

##### BW search with wavelet tree rank query #####
SENTINEL_idx_mis = bwt_mis.index("$")
C_dict_mis = bwt_wt.construct_C(mis)

# WT Node tree
w1_mis = wt1.WaveletTree(bwt_mis.replace("$", "")) # remove sentinel
# WT level order
w2_mis = wt2.WaveletTree(bwt_mis.replace("$", "")) # remove sentinel



def O_hits_mississippi(p):
	return bwt_O.bw_search(bwt_mis, p, sparse_sa_mis, C_mis, O_mis, letter_to_num_dict_mis)

def wt_lvl_hits_mississippi(p):
	return bwt_wt.bw_search(p, bwt_mis, SENTINEL_idx_mis, sparse_sa_mis, C_dict_mis, w1_mis)

def wt_hits_mississippi(p):
	return bwt_wt.bw_search(p, bwt_mis, SENTINEL_idx_mis, sparse_sa_mis, C_dict_mis, w2_mis)



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















