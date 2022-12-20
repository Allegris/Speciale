from numpy.random import choice
from shared import get_alphabet


# DNA alphabet: size 4
alpha = ["A", "C", "G", "T"]
probs = [0.25] * len(alpha)
#probs = [0.4, 0.1, 0.1, 0.4]




'''
# Lorem ipsum alphabet: size 43
x = "1234567Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Sed turpis tincidunt id aliquet risus feugiat in ante metus. Et malesuada fames ac turpis egestas maecenas pharetra. Turpis egestas integer eget aliquet. Semper eget duis at tellus at urna condimentum mattis pellentesque. Phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec sagittis. Sed augue lacus viverra vitae congue eu. Nulla facilisi etiam dignissim diam quis enim lobortis scelerisque fermentum. Non odio euismod lacinia at. Libero justo laoreet sit amet cursus sit amet. Malesuada nunc vel risus commodo viverra maecenas accumsan lacus vel. Ipsum faucibus vitae aliquet nec ullamcorper sit. Viverra mauris in aliquam sem fringilla. Sed augue lacus viverra vitae congue. Hendrerit gravida rutrum quisque non tellus. Turpis nunc eget lorem dolor sed viverra ipsum nunc aliquet. Porttitor rhoncus dolor purus non enim praesent elementum facilisis. Lorem ipsum dolor sit amet consectetur adipiscing elit. At tellus at urna condimentum mattis pellentesque id nibh. Placerat vestibulum lectus mauris ultrices eros in. Massa tincidunt dui ut ornare lectus sit. Nunc mi ipsum faucibus vitae aliquet nec. Dolor sit amet consectetur adipiscing elit ut aliquam. Magna ac placerat vestibulum lectus mauris ultrices eros. Dictum non consectetur a erat nam at lectus. Mattis aliquam faucibus purus in massa. Tellus in metus vulputate eu scelerisque felis imperdiet proin fermentum. Rhoncus dolor purus non enim praesent. Et sollicitudin ac orci phasellus egestas. Vitae nunc sed velit dignissim sodales ut eu sem. In massa tempor nec feugiat nisl. Sagittis aliquam malesuada bibendum arcu vitae elementum. Justo eget magna fermentum iaculis eu non. Ultricies mi quis hendrerit dolor magna. Porta non pulvinar neque laoreet suspendisse. Facilisi nullam vehicula ipsum a arcu cursus vitae congue mauris. Leo vel fringilla est ullamcorper eget nulla facilisi etiam. Id velit ut tortor pretium viverra. Diam sit amet nisl suscipit adipiscing. Posuere sollicitudin aliquam ultrices sagittis orci. Ac tortor vitae purus faucibus ornare suspendisse sed. Diam volutpat commodo sed egestas. Euismod in pellentesque massa placerat duis ultricies lacus sed turpis. Eros donec ac odio tempor orci dapibus ultrices. Massa sed elementum tempus egestas sed sed risus. Amet consectetur adipiscing elit pellentesque habitant. Pharetra pharetra massa massa ultricies mi quis. Nulla facilisi etiam dignissim diam quis. Sagittis eu volutpat odio facilisis mauris. Dolor morbi non arcu risus quis varius quam quisque id. Amet consectetur adipiscing elit duis. Rhoncus aenean vel elit scelerisque mauris pellentesque. Convallis convallis tellus id interdum velit laoreet. Elit sed vulputate mi sit amet mauris commodo quis. Ullamcorper a lacus vestibulum sed arcu non odio euismod lacinia. Platea dictumst quisque sagittis purus sit amet volutpat consequat mauris. Eget est lorem ipsum dolor. Sapien eget mi proin sed libero enim sed faucibus. Orci ac auctor augue mauris augue. Sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus. Viverra ipsum nunc aliquet bibendum. Ipsum dolor sit amet consectetur. Nec tincidunt praesent semper feugiat nibh sed pulvinar proin gravida. Urna molestie at elementum eu facilisis sed odio morbi. Pellentesque habitant morbi tristique senectus. Quam viverra orci sagittis eu volutpat odio facilisis mauris. Consequat ac felis donec et odio pellentesque diam volutpat commodo. Integer feugiat scelerisque varius morbi enim nunc faucibus. Dolor purus non enim praesent. Integer enim neque volutpat ac tincidunt vitae semper."
alpha = get_alphabet(x)
print(len(alpha))
probs = [1 / len(alpha)] * len(alpha) # equal probs
'''

'''
x = "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVXYZ"
alpha = get_alphabet(x) # size 50
probs = [1 / len(alpha)] * len(alpha) # equal probs
'''

def generate_string(n):
	return "".join(choice(alpha, n, p=probs))


def print_to_file(n):
	title = f"simulated_data\\simulated_DNA_n{n}.txt"
	file = open(title, "w")
	file.write(generate_string(n))
	file.close()


##########################################################################
# Code to run
##########################################################################

#file = open("simulated_DNA.txt", "w")
#file.write(common_ancestor(10000000))
#file.close()

#ns = list(range(1000, 10001, 1000)) # 1K
ns = list(range(1000, 10001, 1000)) #  10K
#ns = list(range(10000, 100001, 10000)) # 100K
#ns = list(range(50000, 1000001, 50000)) # 1M

for n in ns:
	print_to_file(n)










