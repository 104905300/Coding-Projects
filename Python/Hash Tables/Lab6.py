# You may not use dicts.
def getName():
	return "Hai Ning Liu"
	
class MyHashTable():
    def __init__(self, size, hash1):
        # Create an empty hashtable with the size given, and stores the function hash1
        self.size = size
        self.hash_func = hash1
        self.table = [None] * self.size
        self.count = 0
        

    def put(self, key, data):
        # Store data with the key given, return true if successful or false if the data cannot be entered
        # On a collision, the table should not be changed

        index = self.hash_func(key)

        if ((not self.isFull()) and (self.table[index] is None)):
            self.table[index] = (key, data)
            self.count = self.count + 1
            return True
        return False

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist
        index = self.hash_func(key)

        if((self.table[index] is None) or (self.table[index][0] != key)):
            # if no element exist or the key isn't correct
            return None

        return self.table[index][1]
        
    def __len__(self):
        # Returns the number of items in the Hash Table
        return self.count

    def isFull(self):
        # Returns true if the HashTable cannot accept new members
        return self.count == self.size


class MyChainTable(MyHashTable):
    def __init__(self, size, hash1):
        # Create an empty hashtable with the size given, and stores the function hash1
        super().__init__(size,hash1)
        self.spotOccupied = 0
    
    def put(self, key, data):
        # Store the data with the key given in a list in the table, return true if successful or false if the data cannot be entered
        # On a collision, the data should be added to the list
        if (self.isFull()):
            return False

        index = self.hash_func(key)
        if (self.table[index] is None):
            # no collison, key and data will be added to a link list
            self.table[index] = Node(key, data)
            self.spotOccupied = self.spotOccupied + 1
        else:
            #collison
            curNode = self.table[index]
            # get the last node
            while (curNode.chain is not None):
                curNode = curNode.chain
            curNode.chain = Node(key, data)
        
        self.count = self.count + 1
        return True

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist
        index = self.hash_func(key)

        curNode = self.table[index]
        while (True):
            if(key == curNode.key):
                return curNode.data
            if(curNode.chain is None):
                return None
            curNode = curNode.chain
        
    def __len__(self):
        # Returns the number of items in the Hash Table
        return self.count

    def isFull(self):
        # Returns true if the HashTable cannot accept new members

        # chainTable can always accept new members because 
        # link list can alwasy chain new members in the case of collison 
        return False


class MyDoubleHashTable(MyHashTable):
    def __init__(self, size, hash1, hash2):
        # Create an empty hashtable with the size given, and stores the functions hash1 and hash2
        super().__init__(size,hash1)
        self.second_hash = hash2

    
    def put(self, key, data):
        # Store data with the key given, return true if successful or false if the data cannot be entered
        # On a collision, the key should be rehashed using some combination of the first and second hash functions
        # Be careful that your code does not enter an infinite loop
        if (self.count == self.size):
            return False

        index = self.hash_func(key)

        # this two variable is to handle collison
        original_index = index
        offset = self.second_hash(index)

        # loop will terminate when an item empty slot is found from offset, 
        # or when we offset back to the same index (no empty spot available)
        while (self.table[index] is not None):

            # loop to the back of the list if new index is less than 0 (circular)
            if (index - offset < 0):
                index = index - offset + self.size
            else: 
                index = index - offset
            
            if (original_index == index):
                # index repeat, can't find free slot to insert (no empty spot available)
                return False
        self.table[index] = (key, data)
        self.count = self.count + 1
        return True

    def get(self, key):
        # Returns the item linked to the key given, or None if element does not exist 
        
        index = self.hash_func(key)

        # this two variable is to handle collison
        original_index = index
        offset = self.second_hash(index)
        
        # keep looping until the correct key is found or item is confirmed does not exist
        while ((self.table[index] is None) or (self.table[index][0] != key)):

            # loop to the back of the list if new index is less than 0 (circular)
            if (index - offset < 0):
                index = index - offset + self.size
            else: 
                index = index - offset
            
            if (original_index == index):
                # return None if offset repeat (the element does not exist),
                return None

        return self.table[index][1]
        
    def __len__(self):
        # Returns the number of items in the Hash Table
        return self.count



class Node:
    def __init__(self, key, data, node=None):
        # Initialize this node, insert data, and set the next node if any
        self.key=key
        self.data=data
        self.chain=node
