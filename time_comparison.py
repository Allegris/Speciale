from random import randrange
import time
import matplotlib.pyplot as plt
from one_hot_encoding import OneHotEncoding
import wavelet_tree as w1
import wavelet_tree_lvl as w2
from bwt_search import Occ
from shared import construct_sa_skew, bwt


def generate_queries(x):
	n = len(x)
	queries = []
	for _ in range(n):
		char_idx = randrange(0, n)
		char = x[char_idx]
		query_idx = randrange(0, n)
		queries.append((char, query_idx))
	return queries


def query_times(queries, ds):
	start = time.time()
	for c, i in queries:
		ds.rank(c, i)
	end = time.time()
	return (end-start)/len(queries)


occ_pre = []
ohe_pre = []
wt1_pre = []
wt2_pre = []

occ_qt = []
ohe_qt = []
wt1_qt = []
wt2_qt = []


#ns = list(range(1000, 10001, 1000)) # 1K
ns = list(range(1000, 10001, 1000)) #  10K
#ns = list(range(10000, 100001, 10000)) # 100K
#ns = list(range(50000, 1000001, 50000)) # 1M

for n in ns:
	print(n)
	title = f"simulated_data\\simulated_Big_n{n}.txt"
	file = open(title, "r")
	x = file.read()
	file.close()

	x += "0"
	sa = construct_sa_skew(x)
	bwt_x = bwt(x, sa)

	queries = generate_queries(bwt_x)


	##### PREPROCESSING TIMES #####
	# One hot encoding
	start = time.time()
	ohe = OneHotEncoding(bwt_x)
	end = time.time()
	ohe_pre.append(end - start)

	# WT node object
	start = time.time()
	wt1 = w1.WaveletTree(bwt_x)
	end = time.time()
	wt1_pre.append(end - start)

	# WT level
	start = time.time()
	wt2 = w2.WaveletTree(bwt_x)
	end = time.time()
	wt2_pre.append(end - start)

	# Occ
	start = time.time()
	occ = Occ(bwt_x)
	end = time.time()
	occ_pre.append(end - start)


	##### QUERY TIMES #####
	# One hot encoding
	ohe_time = query_times(queries, ohe)
	ohe_qt.append(ohe_time)

	# WT node object
	wt1_time = query_times(queries, wt1)
	wt1_qt.append(wt1_time)

	# WT level
	wt2_time = query_times(queries, wt2)
	wt2_qt.append(wt2_time)

	# Occ
	occ_time = query_times(queries, occ)
	occ_qt.append(occ_time)




##### STORE RESULTS AND PLOTS #####

f = open("Results\\TIME\\times.txt", "w")
f.write("PREPROCESSING TIMES:\n")
f.write("Occ: " + str(occ_pre) + "\n")
f.write("Ohe: " + str(ohe_pre) + "\n")
f.write("WT1: " + str(wt1_pre) + "\n")
f.write("WT2: " + str(wt2_pre) + "\n")
f.write("\nQUERY TIMES:\n")
f.write("Occ: " + str(occ_qt) + "\n")
f.write("Ohe: " + str(ohe_qt) + "\n")
f.write("WT1: " + str(wt1_qt) + "\n")
f.write("WT2: " + str(wt2_qt) + "\n")
f.close()


plt.plot(ns, occ_pre, color = "red", marker='o', label = "Occ", alpha = 0.6) #, linestyle = 'None'
plt.plot(ns, ohe_pre, color = "blue", marker='o', label = "OHE", alpha = 0.6)
plt.plot(ns, wt1_pre, color = "orange", marker='o', label = "WT", alpha = 0.9)
plt.plot(ns, wt2_pre, color = "green", marker='o', label = "WT_lvl", alpha = 0.6)
plt.xlabel("n", fontsize = 13)
plt.ylabel("Preprocessing time (sec)", fontsize = 13)
plt.legend(loc = 'upper left')
plt.tight_layout()
plt.savefig("Results\\TIME\\Time_preprocessing_all_Big")
plt.show()
plt.clf() # Clear plot


plt.plot(ns, occ_qt, color = "red", marker='o', label = "Occ", alpha = 0.6)
plt.plot(ns, ohe_qt, color = "blue", marker='o', label = "OHE", alpha = 0.6)
plt.plot(ns, wt1_qt, color = "orange", marker='o', label = "WT", alpha = 0.9)
plt.plot(ns, wt2_qt, color = "green", marker='o', label = "WT_lvl", alpha = 0.6)
plt.xlabel("n", fontsize = 13)
plt.ylabel("Rank query time (sec)", fontsize = 13)
plt.legend(loc = 'upper left')
plt.tight_layout()
plt.savefig("Results\\TIME\\Time_query_all_Big")
plt.show()
plt.clf() # Clear plot

