import sys
import one_hot_encoding as ohe
import wavelet_tree as wt
import wavelet_tree_lvl as wt_lvl
from shared import huffman_codes

def get_size(obj, seen=None):
    # Recursively find size of objects
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size



#x = "mississippi$" #"ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789" #+ "A"*10000 + "B"*10000
#x = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789"
file = open("simulated_DNA.txt", "r")
x = file.read()
file.close()

ohe_table = ohe.one_hot_encoding(x)
ohe_ranks = ohe.preprocess_ranks(ohe_table, len(x))
ohe_size = get_size(ohe_table) + get_size(ohe_ranks)
print("Size of OHE:", ohe_size)

wt_root = wt.WaveletTreeNode(x, 0, None) # x, level, root
wt_size = get_size(wt_root)
print("Size of WT Nodes:", wt_size)

codes = huffman_codes(x)
wt, child_dict = wt_lvl.wavelet_tree(x, codes)
ranks = wt_lvl.all_node_ranks(wt, len(x), child_dict)
wt_lvl_size = get_size(codes) + get_size(wt) + get_size(child_dict) + get_size(ranks)
print("Size of WT lvl:", wt_lvl_size)








