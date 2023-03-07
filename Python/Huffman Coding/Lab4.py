import heapq


def getName():
    return "Hai Ning Liu"


class MyHuffman:
    def __init__(self):
        # Initialize the Huffman tree

        # dictionary to hold the characters and their coressponding bitcode
        self.chars = {}
        # Huffman tree
        self.tree = None
        # position in the bitstring being decoded
        self.decodePosition = 0

    def build(self, weights):
        # Build a huffman tree from the dictionary of character:value pairs

        # create a node heap (heap containing all the nodes) that contains all 
        # characters and their corrsponding frequency. 

        node_heap = []
        # add all nodes to heap
        for character, frequency in weights.items():
            # right now node_heap is still a list
            node_heap.append(Node(character,frequency))

        # heapify will sort the list into a heap (min heap)
        heapq.heapify(node_heap)

        created_node_order = 1

        # build tree until there is only one node left, 
        # and that node is the root (huffman tree built complete)
        while (len(node_heap) != 1):
            # get the two tuple with the lowest frequency
            # heappush and heappop will auto heapify after
            min_node = heapq.heappop(node_heap)
            second_min_node = heapq.heappop(node_heap)

            # create the combined non character node and put it in heap 
            created_node = Node(None, (min_node.frequency + second_min_node.frequency),
                min_node, second_min_node, created_node_order)

            created_node_order = created_node_order + 1

            heapq.heappush(node_heap, created_node)
        
        # the last node in node_heap is the root which is also the tree
        self.tree = heapq.heappop(node_heap)

        self.makeLookupTable(self.tree, "")


    def makeLookupTable(self, node, bitCode):
        # Recursive algorithm to fill the dictionay of characters with their coressponding bitcode
        if (node is None):
            return
        if ((node.left is None) and (node.right is None)):
            self.chars[node.character]= bitCode
        
        if (node.left is not None):
            self.makeLookupTable(node.left, bitCode + "1")
        
        if (node.right is not None):
            self.makeLookupTable(node.right, bitCode + "0")


    def encode(self, word):
        # Return the bitstring of word encoded by the rules of your huffman tree
        bitString = ""
        for char in word:
            bitString = bitString + self.chars[char]

        return bitString


    def decode(self, bitstring):
        # Return the word encoded in bitstring, or None if the code is invalid
        word = ""
        cur_node = self.tree

        for bit in bitstring:
            if (bit == "1"):
                cur_node = cur_node.left
            else:
                cur_node = cur_node.right

            if ((cur_node.left is None) and (cur_node.right is None)):
                # if it's leaf node than we can append a character
                word = word + cur_node.character
                # go back to root for the next character after a character is found 
                cur_node = self.tree
        
        return word


    def recursiveTraverseTree(self, node, bitString):
        # Return the character after traversing the Huffman tree through the bitstring

        if (len(bitString) == self.decodePosition):
            # after finish, reset position back to 0 for future use
            self.decodePosition = 0
            return node.character

        if (bitString[self.decodePosition] == "1"):
            self.decodePosition = self.decodePosition + 1
            return self.recursiveTraverseTree(node.left, bitString)
        else:
            self.decodePosition = self.decodePosition + 1
            return self.recursiveTraverseTree(node.right, bitString)


# This node structure might be useful to you
class Node:
    def __init__(self, character, frequency, left=None, right=None, creation_order=None):
        # creation order is used when two creation node is the same frequency, 
        # in which the smaller node is the one created eariler (lower creation order), 
        self.character = character
        self.frequency = frequency
        self.left = left
        self.right = right
        self.creation_order = creation_order

    def __eq__(self, other):
        # in practice, this should be always false for huffman tree
        return ((self.character == other.character) and (self.frequency == other.frequency))

    def __ne__(self, other):
        # they are not equal when one of the following condition is true
        # in practice, this should be always true for huffman tree
        return ((self.character != other.character) or (self.frequency != other.frequency))

    def __le__(self, other):
        # if self is less than other

        if (self.frequency == other.frequency):
            # when both node frequency is equal, the following rules 
            # will determine which node is bigger/smaller
            if ((self.creation_order == None) and (other.creation_order == None)):
                # both are character node
                return self.character <= other.character
            elif ((self.creation_order != None) and (other.creation_order == None)):
                # if self is the created node and other isn't, self is smaller
                return True
            elif ((self.creation_order == None) and (other.creation_order != None)):
                # if self is not created node and other is, self is bigger
                return False
            else:
                # both are created node, the one with the lower order is smaller
                return self.creation_order <= other.creation_order
        else:
            return (self.frequency <= other.frequency)
    
    def __lt__(self, other):
        # less than and less or equal than has the same defintion in this case 
        # because no two huffman tree nodes can be the same
        return self.__le__(other)

    def __ge__(self, other):
        return not(self.__le__(other))

    def __gt__(self, other):
        return not(self.__lt__(other))
