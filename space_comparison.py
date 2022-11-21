import sys
import matplotlib.pyplot as plt
from one_hot_encoding import one_hot_encoding, preprocess_ranks
from wavelet_tree import WaveletTree
from wavelet_tree_lvl import WaveletTree
from bwt_search import construct_O, map_string_to_ints
from shared import construct_sa_skew


# Credit: https://goshippo.com/blog/measure-real-size-any-python-object/
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


if __name__ == "__main__":
	#ns = [100, 1000, 10000, 100000, 1000000, 10000000]
	#ns = [100000, 1000000, 10000000]
	ns = list(range(500, 10001, 500))
	o_ls = []
	ohe_ls = []
	wt_node_ls = []
	wt_lvl_ls = []

	for n in ns:
		print("n", n)
		title = f"simulated_data\\simulated_DNA_n{n}.txt"
		file = open(title, "r")
		x = file.read()
		file.close()

		# One hot encoding
		summ = 0
		for _ in range(10):
			ohe_table = one_hot_encoding(x)
			ohe_ranks = preprocess_ranks(ohe_table, len(x))
			ohe_size =  get_size(ohe_table) + get_size(ohe_ranks)
			summ += ohe_size
		ohe_ls.append(summ/10)

		# Wavelet tree - node representation
		summ = 0
		for _ in range(10):
			wt = WaveletTree(x)
			summ += get_size(wt)
		#wt_node_ls.append(get_size(wt))
		wt_node_ls.append(summ/10)


		# Wavelet tree - level order representation
		summ = 0
		for _ in range(10):
			wt2 = wavelet_tree(x)
			summ += get_size(wt2)
		wt_lvl_ls.append(summ/10)

		# O table
		x += "0" # Add sentinel to x - needed by Skew
		sa = construct_sa_skew(x)
		num_to_letter_dict, _, _ = map_string_to_ints(x)
		summ = 0
		for _ in range(10):
			O = construct_O(x, sa, num_to_letter_dict)
			summ += get_size(O)
		#o_ls.append(get_size(O))
		o_ls.append(summ/10)


	##### PLOTS #####

	print("n:", ns)
	print("occ:", o_ls)
	print("ohe:", ohe_ls)
	print("wt:", wt_node_ls)
	plt.scatter(ns, o_ls, color = "red", s=50, alpha = 0.5)
	plt.scatter(ns, ohe_ls, color = "orange", s=50, alpha = 0.5)
	plt.scatter(ns, wt_node_ls, color = "blue", s=50, alpha = 0.5)
	plt.scatter(ns, wt_lvl_ls, color = "green", s=50, alpha = 0.5)
	#plt.ylim(0, 6*(10**(-6)))
	#plt.xscale("log", basex = 10)
	#plt.yscale("log", basey = 10)
	plt.xlabel("n", fontsize = 13)
	plt.ylabel("Memory usage (bytes)", fontsize = 13)
	plt.savefig("Space_usage_random")
	plt.show()
	plt.clf() # Clear plot




