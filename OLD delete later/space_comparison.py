import tracemalloc
import wavelet_tree as tree
import wavelet_tree_level_order_pointers as lo
import one_hot_encoding as ohe
from shared import huffman_codes

#x = "ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ123456789AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
'''
x = "a" * 1000000
x += "b" * 1000000
x += "c" * 100000
x += "d" * 100000
x += "efghi"
'''

x = "a" * 10000000 + "bcdefghijklmnopqrstuvwxyz"

#x = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet justo donec enim diam vulputate. Id eu nisl nunc mi ipsum. Eget est lorem ipsum dolor sit amet consectetur adipiscing. Nisl pretium fusce id velit ut tortor pretium viverra. Felis eget velit aliquet sagittis id. Orci porta non pulvinar neque laoreet. Nulla pellentesque dignissim enim sit amet. Dui sapien eget mi proin sed libero. Arcu ac tortor dignissim convallis aenean et tortor at. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Laoreet suspendisse interdum consectetur libero. Dictum at tempor commodo ullamcorper a lacus. Integer feugiat scelerisque varius morbi enim nunc faucibus a pellentesque. Auctor augue mauris augue neque gravida in fermentum et sollicitudin. Tortor id aliquet lectus proin. Adipiscing enim eu turpis egestas pretium aenean pharetra magna. Tristique nulla aliquet enim tortor at auctor."
#x = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet justo donec enim diam vulputate. Id eu nisl nunc mi ipsum. Eget est lorem ipsum dolor sit amet consectetur adipiscing. Nisl pretium fusce id velit ut tortor pretium viverra. Felis eget velit aliquet sagittis id. Orci porta non pulvinar neque laoreet. Nulla pellentesque dignissim enim sit amet. Dui sapien eget mi proin sed libero. Arcu ac tortor dignissim convallis aenean et tortor at. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Laoreet suspendisse interdum consectetur libero. Dictum at tempor commodo ullamcorper a lacus. Integer feugiat scelerisque varius morbi enim nunc faucibus a pellentesque. Auctor augue mauris augue neque gravida in fermentum et sollicitudin. Tortor id aliquet lectus proin. Adipiscing enim eu turpis egestas pretium aenean pharetra magna. Tristique nulla aliquet enim tortor at auctor. Ac orci phasellus egestas tellus rutrum tellus pellentesque eu. Accumsan lacus vel facilisis volutpat est velit egestas dui. Nisi est sit amet facilisis magna etiam tempor orci eu. Lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque. Natoque penatibus et magnis dis parturient montes nascetur. Integer vitae justo eget magna fermentum iaculis eu. Imperdiet sed euismod nisi porta. Sed sed risus pretium quam vulputate dignissim suspendisse in. Tempor orci dapibus ultrices in iaculis nunc sed augue. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet. Mattis vulputate enim nulla aliquet porttitor. Tristique et egestas quis ipsum. Faucibus vitae aliquet nec ullamcorper sit amet risus nullam. Mi tempus imperdiet nulla malesuada. Gravida in fermentum et sollicitudin. Venenatis tellus in metus vulputate eu scelerisque. Tristique nulla aliquet enim tortor at auctor. Sit amet porttitor eget dolor morbi non arcu. Tincidunt eget nullam non nisi est sit amet facilisis. Vitae elementum curabitur vitae nunc sed. Varius vel pharetra vel turpis nunc eget lorem. Nulla porttitor massa id neque aliquam vestibulum morbi blandit. Adipiscing commodo elit at imperdiet dui accumsan sit amet nulla. Dictum varius duis at consectetur lorem donec massa sapien faucibus. Nunc congue nisi vitae suscipit tellus mauris. Proin sagittis nisl rhoncus mattis rhoncus urna. Elementum nisi quis eleifend quam adipiscing. Vivamus arcu felis bibendum ut tristique et egestas quis ipsum. Eget mauris pharetra et ultrices neque. Arcu vitae elementum curabitur vitae. Morbi enim nunc faucibus a pellentesque sit amet. Sagittis aliquam malesuada bibendum arcu vitae elementum. Nulla aliquet porttitor lacus luctus accumsan tortor posuere. Enim diam vulputate ut pharetra sit amet aliquam. Risus feugiat in ante metus dictum at. In massa tempor nec feugiat nisl pretium fusce. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum. Ut lectus arcu bibendum at varius. Nisl suscipit adipiscing bibendum est ultricies integer quis auctor elit. Ultricies mi quis hendrerit dolor. Malesuada fames ac turpis egestas maecenas pharetra convallis posuere. Habitant morbi tristique senectus et netus et malesuada fames ac. Morbi quis commodo odio aenean sed adipiscing diam. Et netus et malesuada fames. At volutpat diam ut venenatis tellus. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue eget. Amet aliquam id diam maecenas ultricies mi. Eget est lorem ipsum dolor sit. Faucibus pulvinar elementum integer enim neque. Sollicitudin aliquam ultrices sagittis orci. Metus aliquam eleifend mi in nulla posuere. Cursus metus aliquam eleifend mi in nulla. Tellus in metus vulputate eu. Libero justo laoreet sit amet cursus sit amet. Tristique et egestas quis ipsum."
#x = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sit amet justo donec enim diam vulputate. Id eu nisl nunc mi ipsum. Eget est lorem ipsum dolor sit amet consectetur adipiscing. Nisl pretium fusce id velit ut tortor pretium viverra. Felis eget velit aliquet sagittis id. Orci porta non pulvinar neque laoreet. Nulla pellentesque dignissim enim sit amet. Dui sapien eget mi proin sed libero. Arcu ac tortor dignissim convallis aenean et tortor at. Eu tincidunt tortor aliquam nulla facilisi cras fermentum odio. Consectetur adipiscing elit duis tristique sollicitudin nibh sit amet. Laoreet suspendisse interdum consectetur libero. Dictum at tempor commodo ullamcorper a lacus. Integer feugiat scelerisque varius morbi enim nunc faucibus a pellentesque. Auctor augue mauris augue neque gravida in fermentum et sollicitudin. Tortor id aliquet lectus proin. Adipiscing enim eu turpis egestas pretium aenean pharetra magna. Tristique nulla aliquet enim tortor at auctor. Ac orci phasellus egestas tellus rutrum tellus pellentesque eu. Accumsan lacus vel facilisis volutpat est velit egestas dui. Nisi est sit amet facilisis magna etiam tempor orci eu. Lorem ipsum dolor sit amet consectetur adipiscing elit pellentesque. Natoque penatibus et magnis dis parturient montes nascetur. Integer vitae justo eget magna fermentum iaculis eu. Imperdiet sed euismod nisi porta. Sed sed risus pretium quam vulputate dignissim suspendisse in. Tempor orci dapibus ultrices in iaculis nunc sed augue. Facilisi morbi tempus iaculis urna id volutpat lacus laoreet. Mattis vulputate enim nulla aliquet porttitor. Tristique et egestas quis ipsum. Faucibus vitae aliquet nec ullamcorper sit amet risus nullam. Mi tempus imperdiet nulla malesuada. Gravida in fermentum et sollicitudin. Venenatis tellus in metus vulputate eu scelerisque. Tristique nulla aliquet enim tortor at auctor. Sit amet porttitor eget dolor morbi non arcu. Tincidunt eget nullam non nisi est sit amet facilisis. Vitae elementum curabitur vitae nunc sed. Varius vel pharetra vel turpis nunc eget lorem. Nulla porttitor massa id neque aliquam vestibulum morbi blandit. Adipiscing commodo elit at imperdiet dui accumsan sit amet nulla. Dictum varius duis at consectetur lorem donec massa sapien faucibus. Nunc congue nisi vitae suscipit tellus mauris. Proin sagittis nisl rhoncus mattis rhoncus urna. Elementum nisi quis eleifend quam adipiscing. Vivamus arcu felis bibendum ut tristique et egestas quis ipsum. Eget mauris pharetra et ultrices neque. Arcu vitae elementum curabitur vitae. Morbi enim nunc faucibus a pellentesque sit amet. Sagittis aliquam malesuada bibendum arcu vitae elementum. Nulla aliquet porttitor lacus luctus accumsan tortor posuere. Enim diam vulputate ut pharetra sit amet aliquam. Risus feugiat in ante metus dictum at. In massa tempor nec feugiat nisl pretium fusce. Eget lorem dolor sed viverra ipsum nunc aliquet bibendum. Ut lectus arcu bibendum at varius. Nisl suscipit adipiscing bibendum est ultricies integer quis auctor elit. Ultricies mi quis hendrerit dolor. Malesuada fames ac turpis egestas maecenas pharetra convallis posuere. Habitant morbi tristique senectus et netus et malesuada fames ac. Morbi quis commodo odio aenean sed adipiscing diam. Et netus et malesuada fames. At volutpat diam ut venenatis tellus. Ullamcorper dignissim cras tincidunt lobortis feugiat vivamus at augue eget. Amet aliquam id diam maecenas ultricies mi. Eget est lorem ipsum dolor sit. Faucibus pulvinar elementum integer enim neque. Sollicitudin aliquam ultrices sagittis orci. Metus aliquam eleifend mi in nulla posuere. Cursus metus aliquam eleifend mi in nulla. Tellus in metus vulputate eu. Libero justo laoreet sit amet cursus sit amet. Tristique et egestas quis ipsum." * 3000

'''
file = open("simulated_DNA.txt", "r")
x = file.read()
file.close()
'''

ohe_ls = []
tree_ls = []
lo_ls = []

ohe_ls_peak = []
tree_ls_peak = []
lo_ls_peak = []


for _ in range(1):

	# OHE
	tracemalloc.start()
	d = ohe.one_hot_encoding(x)
	ohe_ranks = ohe.preprocess_ranks(d, len(x))
	ohe_ls.append(tracemalloc.get_traced_memory()[0])
	ohe_ls_peak.append(tracemalloc.get_traced_memory()[1])
	tracemalloc.stop()

	# Node tree
	tracemalloc.start()
	root = tree.WaveletTreeNode(x, 0, None)
	tree_ls.append(tracemalloc.get_traced_memory()[0])
	tree_ls_peak.append(tracemalloc.get_traced_memory()[1])
	tracemalloc.stop()

	# Level order tree
	tracemalloc.start()
	codes = huffman_codes(x)
	wt, pointers = lo.wavelet_tree(x, codes)
	ranks = lo.preprocess_all_tree_node_ranks(wt, len(x), pointers)
	lo_ls.append(tracemalloc.get_traced_memory()[0])
	lo_ls_peak.append(tracemalloc.get_traced_memory()[1])
	tracemalloc.stop()

print("CURRENT")
print("Type, min, max, avr")
print("Node", min(tree_ls), max(tree_ls), sum(tree_ls)/len(tree_ls))
print("Lvl.", min(lo_ls), max(lo_ls), sum(lo_ls)/len(lo_ls))
print("Ohe.", min(ohe_ls), max(ohe_ls), sum(ohe_ls)/len(ohe_ls))

print("PEAK")
print("Type, min, max, avr")
print("Node", min(tree_ls_peak), max(tree_ls_peak), sum(tree_ls_peak)/len(tree_ls_peak))
print("Lvl.", min(lo_ls_peak), max(lo_ls_peak), sum(lo_ls_peak)/len(lo_ls_peak))
print("Ohe.", min(ohe_ls_peak), max(ohe_ls_peak), sum(ohe_ls_peak)/len(ohe_ls_peak))

'''
tracemalloc.get_traced_memory()
Get the current size and peak size of memory blocks traced by the tracemalloc module as a tuple: (current: int, peak: int).
'''