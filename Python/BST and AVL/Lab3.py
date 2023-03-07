def getName():
    # This method must return your name EXACTLY as D2L presents it.
    # If this does not work, you will fail this lab.
    return "Hai Ning Liu"


class MyBST:
    def __init__(self, data, promote_right=True):
        # Initialize this node, and store data in it
        self.data = data
        self.left = None
        self.right = None
        self.height = 0

        # Set promote_right to TRUE if you are implementing
        # the promotion of the smallest node on left subtree,
        # Otherwise, set it to FALSE
        self.promote_right = promote_right

    def getLeft(self):
        # Return the left child of this node, or None
        return self.left

    def getRight(self):
        # Return the right child of this node, or None
        return self.right

    def getData(self):
        # Return the data contained in this node
        return self.data

    def getHeight(self):
        # Return the height of this node
        return self.height

    def updateHeight(self):
        if ((self.left is None) and (self.right is None)):
            self.height = 0
        elif (self.left is None):
            self.height = self.right.height + 1
        elif (self.right is None):
            self.height = self.left.height + 1
        else:
            self.height = max(self.left.getHeight(), self.right.getHeight()) + 1

    def __contains__(self, data):        
        cur = self
        while (cur is not None):
            if data < cur.data:
                # data to be found smaller than current node, so go left
                cur = cur.left
            elif data > cur.data:
                # data to be found bigger than current node, so go right
                cur = cur.right
            else:
                # node found!
                return True
        # if code reach here that means node not found
        return False
        # Returns true if data is in this node or a node descending from it

    def insert(self, data):
        # Insert data into the tree, descending from this node
        # Ensure that the tree remains a valid Binary Search Tree
        # Return this node after data has been inserted
        if data < self.data:
            if self.left:
                self.left.insert(data)
            else:
                self.left = MyBST(data)
        else:
            if self.right:
                self.right.insert(data)
            else:
                self.right = MyBST(data)
        self.updateHeight()
        return self

    def findSmallest(self):
        if (self is None):
            return None
        
        cur = self
        while (cur.left is not None):
            cur = cur.left

        return cur.getData()

        # Return the value of the smallest node

    def findLargest(self):
        if (self is None):
            return None
        
        cur = self
        while (cur.right is not None):
            cur = cur.right

        return cur.getData()

        # Return the value of the largest node

    def remove(self, data):
        # step 1: find the node to be removed
        # step 2: find new value that will replace value of current node (smallest from right) 
        # step 3: on the node to be removed, replace current value with that new value
        # Step 4: remove the node that you copied the new value from (smallest from right)
        # step 5: update height for all the nodes you traverse down (via return from recursion)

        # find the node to be removed
        if (self is None):
            # the node to be removed does not exist
            return self
        else:
            if data < self.data:
                if (self.left):
                    self.left = self.left.remove(data)
                else:
                    return self
            elif data > self.data:
                if (self.right):
                    self.right = self.right.remove(data)
                else:
                    return self
            else:
                # node to be removed found!

                # if node to be removed have 1 or no child
                if (self.left is None):
                    successor_node = self.right
                    self = None
                    return successor_node
                elif (self.right is None):
                    successor_node = self.left
                    self = None
                    return successor_node

                # node to be removed have 2 children

                # can choose largest from left or smallest from right, 
                # I chose smallest from right in this case
                successor_data = self.right.findSmallest()
                self.data = successor_data

                # removed the copied data from right subtree 
                # (since node have two children, self.right can't be none)
                self.right = self.right.remove(successor_data)
            
            self.updateHeight()
            return self

        # Remove find the data in the input parameter and remove it
        # Ensure that the tree remains a valid Binary Search Tree
        # Return this node after data has been inserted


class MyAVL(MyBST):
    def __init__(self, data):
        # Initialize this node, and store data in it
        super().__init__(data)
        self.bf = 0

    def reBalance(self):
        if (self is None):
            return None

        # need to update bf after rebalance!
        # if right rotate, change bf of itself and right child
        # if left rotate, change bf of itself and left child
        if (self.getBalanceFactor() > 1):
            # left heavy (so self.left can't be None)
            if (self.left.getBalanceFactor() >= 0):
                return self.rightRotate()
            elif (self.left.getBalanceFactor() < 0):
                # double rotate
                # firstly left rotate the left child, 
                # then right rotate the entire thing
                self.left = self.left.leftRotate()
                return self.rightRotate()
        elif (self.getBalanceFactor() < -1):
            # right heavy (so self.right can't be None)
            # always do single rotate over 
            # double rotate if both are correct
            if (self.right.getBalanceFactor() <= 0):
                return self.leftRotate()
            elif (self.right.getBalanceFactor() > 0):
                # double rotate
                self.right = self.right.rightRotate()
                return self.leftRotate()
        
        return self
            
        # Check to see if the current node is out of balance
        # Rebalance it if necessary

    def getBalanceFactor(self):
        if (self is None):
            return 0

        if ((self.left is None) and (self.right is None)) :
            bf = 0
        elif (self.left is None):
            bf = (-1) - self.right.height 
        elif (self.right is None):
            bf =  self.left.height - (-1)
        else:
            bf = self.left.height - self.right.height
        return bf
        # Return the balance factor of this node

    def insert(self, data):
        # Insert data into the tree, descending from this node
        # Ensure that the tree remains a valid AVL tree
        # Return the node in this node's position after data has been inserted

        # after insert, it will find unbalance in the most basic subtree level (not from root) 
        if data < self.data:
            if self.left:
                self.left = self.left.insert(data)
            else:
                self.left = MyAVL(data)
        else:
            if self.right:
                self.right = self.right.insert(data)
            else:
                self.right = MyAVL(data)
        self.updateHeight()
        self.bf = self.getBalanceFactor()
        new = self.reBalance()
        return new

    def leftRotate(self):
        # Perform a left rotation on this node and return the new node in its spot
        new = self.getRight()
        self.right = new.getLeft()
        new.left = self
        new.left.updateHeight()
        new.updateHeight()
        return new

    def rightRotate(self):
        # Perform a right rotation on this node and return the new node in its spot
        new = self.getLeft()
        self.left = new.getRight()
        new.right = self
        new.right.updateHeight()
        new.updateHeight()
        return new

    def remove(self, data):
        # step 1-5: same as BST remove()
        # step 6: update balance factor
        # step 7: balance all nodes that you traverse down (if neccessary)
        # (you don't need to update bf again after balance because bf is 
        # not a value, it's only serve as info on whether you need to balance or not)

        if (self is None):
            # the node to be removed does not exist
            return self
        else:
            if data < self.data:
                # check if there is a left data
                if (self.left):
                    self.left = self.left.remove(data)
                else:
                    return self
            elif data > self.data:
                if (self.right):
                    self.right = self.right.remove(data)
                else:
                    return self
            else:
                # node to be removed found!

                # if node to be removed have 1 or no child
                if (self.left is None):
                    successor_node = self.right
                    self = None
                    return successor_node
                elif (self.right is None):
                    successor_node = self.left
                    self = None
                    return successor_node

                # node to be removed have 2 children

                # can choose largest from left or smallest from right, 
                # I chose smallest from right in this case
                successor_data = self.right.findSmallest()
                self.data = successor_data

                # removed the copied data from right subtree
                self.right = self.right.remove(successor_data)

            self.updateHeight()
            self.bf = self.getBalanceFactor()
            balanced_tree = self.reBalance()
            return balanced_tree


        # Remove find the data in the input parameter and remove it
        # Ensure that the tree remains a valid AVL tree
        # Return the node in this node's position after data has been inserted


# Bonus functions to help you debug
def printTree_(tree, prefix):
    if tree.getLeft() is not None:
        printTree_(tree.getLeft(), prefix + "+ ")
    print(f"{prefix}{tree.data}")
    if tree.getRight() is not None:
        printTree_(tree.getRight(), prefix + "- ")


def printTree(tree):
    printTree_(tree, "")
