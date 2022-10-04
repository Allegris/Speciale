import sys
#import one_hot_encoding as ohe
#import wavelet_tree as wt_node
#import wavelet_tree_lvl as wt_lvl
from one_hot_encoding import one_hot_encoding, preprocess_ranks
from wavelet_tree import WaveletTreeNode
from wavelet_tree_lvl import wavelet_tree

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

ohe_table = one_hot_encoding(x)
ohe_ranks = preprocess_ranks(ohe_table, len(x))
ohe_size = get_size(ohe_table) + get_size(ohe_ranks)
print("Size of OHE:", ohe_size)

wt_root = WaveletTreeNode(x, 0, None) # x, level, root
print("Size of WT Nodes:", get_size(wt_root))

wt2 = wavelet_tree(x)
print("Size of WT lvl:", get_size(wt2))








