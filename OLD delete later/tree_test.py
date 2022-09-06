class WaveletTreeNode:
    def __init__(self, bv):
        self.bv = bv
        self.leftChild = None
        self.rightChild = None


node1 = WaveletTreeNode(50)
node2 = WaveletTreeNode(20)
node3 = WaveletTreeNode(45)

node1.leftChild = node2
node1.rightChild = node3



print("node1", node1)
print("node2", node2)
print("node3", node3)

print("node1.leftChild", node1.leftChild)
print("node1.leftChildaaa", node1.leftChild.leftChild)
node2.leftChild = node3
print("node1.leftChildbbb", node1.leftChild.leftChild)
