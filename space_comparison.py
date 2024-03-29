import sys
import matplotlib.pyplot as plt
from one_hot_encoding import OneHotEncoding
import wavelet_tree as w1
import wavelet_tree_lvl as w2
from bwt_search import Occ


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



def init_file(filename):
	f = open(filename, "w")
	f.write("\"n\"," + "\"bytes\"" + "\n")
	f.close()



def write_to_file(filename, n, s):
	f = open(filename, "a")
	f.write(str(n) + "," + str(s) + "\n")
	#f.write("\"" + str(i+1) + "\"" + "," + str(n) + "," + str(s) + "\n")
	f.close()



dna_big = "Big" # "DNA"
path = f"Results\\SPACE\\{dna_big}\\"

if __name__ == "__main__":
	init_file(path + "data_ohe.txt")
	init_file(path + "data_wt.txt")
	init_file(path + "data_wt2.txt")
	init_file(path + "data_occ.txt")

	#ns = list(range(1000, 10001, 1000)) # 1K
	ns = list(range(1000, 10001, 1000)) #  10K
	#ns = list(range(10000, 100001, 10000)) # 100K
	#ns = list(range(50000, 1000001, 50000)) # 1M

	o_ls = []
	ohe_ls = []
	wt_node_ls = []
	wt_lvl_ls = []

	for i, n in enumerate(ns):
		print("n", n)
		title = f"simulated_data\\simulated_{dna_big}_n{n}.txt"
		file = open(title, "r")
		x = file.read()
		file.close()

		# One hot encoding
		ohe = OneHotEncoding(x)
		s = get_size(ohe)
		ohe_ls.append(s)
		write_to_file(path + "data_ohe.txt", n, s)

		# Wavelet tree - node object representation
		wt1 = w1.WaveletTree(x)
		s = get_size(wt1)
		wt_node_ls.append(s)
		write_to_file(path + "data_wt.txt", n, s)

		# Wavelet tree - level order representation
		wt2 = w2.WaveletTree(x)
		s = get_size(wt2)
		wt_lvl_ls.append(s)
		write_to_file(path + "data_wt2.txt", n, s)

		# Occ table
		occ = Occ(x)
		s = get_size(occ)
		o_ls.append(s)
		write_to_file(path + "data_occ.txt", n, s)



	##### PLOTS #####

	# ALl
	plt.plot(ns, o_ls, color = "red", marker='o', label = "Occ", alpha = 0.6) #, linestyle = 'None'
	plt.plot(ns, ohe_ls, color = "blue", marker='o', label = "OHE", alpha = 0.6)
	plt.plot(ns, wt_node_ls, color = "orange", marker='o', label = "WT", alpha = 0.9)
	plt.plot(ns, wt_lvl_ls, color = "green", marker='o', label = "WT_lvl", alpha = 0.6)
	plt.xlabel("n", fontsize = 13)
	plt.ylabel("Memory usage (bytes)", fontsize = 13)
	plt.legend()
	plt.tight_layout()
	plt.savefig(path + "Space_comparison_all_" + dna_big)
	plt.show()
	plt.clf() # Clear plot


	# OHE, WT1, WT2
	plt.plot(ns, ohe_ls, color = "blue", marker='o', label = "OHE", alpha = 0.6)
	plt.plot(ns, wt_node_ls, color = "orange", marker='o', label = "WT", alpha = 0.9)
	plt.plot(ns, wt_lvl_ls, color = "green", marker='o', label = "WT_lvl", alpha = 0.6)
	plt.xlabel("n", fontsize = 13)
	plt.ylabel("Memory usage (bytes)", fontsize = 13)
	plt.legend()
	plt.tight_layout()
	plt.savefig(path + "Space_comparison_ohe_wts_" + dna_big)
	plt.show()
	plt.clf() # Clear plot


	# WT_node, WT_lvl
	plt.plot(ns, wt_node_ls, color = "orange", marker='o', label = "WT", alpha = 0.9)
	plt.plot(ns, wt_lvl_ls, color = "green", marker='o', label = "WT_lvl", alpha = 0.6)
	plt.xlabel("n", fontsize = 13)
	plt.ylabel("Memory usage (bytes)", fontsize = 13)
	plt.legend()
	plt.tight_layout()
	plt.savefig(path + "Space_comparison_wts_" + dna_big)
	plt.show()
	plt.clf() # Clear plot


