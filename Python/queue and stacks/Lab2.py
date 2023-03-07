def getName():
    # This method must return your name EXACTLY as D2L presents it.
    # If this does not work, you will fail this lab.
    return "Hai Ning Liu"


class Node:
    def __init__(self, data, node=None):
        # Initialize this node, insert data, and set the next node if any
        self.data = data
        self.chain = node

class MyStack:
    def __init__(self, data=None):
        # Initialize this stack, and store data if it exists
        self.length = 0     
        if (data is not None):
            self.topitem = Node(data)
            self.length = self.length + 1
        else:
            self.topitem = None
        

    def push(self, data):
        # Add data to the beginning of the stack
        if (self.topitem is None):
            self.topitem = Node(data)
        else:
            new_node = Node(data)
            new_node.chain = self.topitem
            self.topitem = new_node

        self.length = self.length + 1


    def pop(self):
        # Remove the element at the beginning of the stack.
        # Return the data in the element at the beginning of the stack, or None if the stack is empty
        if (self.topitem is None):
            return None
        else:
            # Record the top item as temp, then redirect new head, 
            # then set chain of previous head to none, then return the popped data
            temp = self.topitem
            self.topitem =  self.topitem.chain
            temp.chain = None
            self.length = self.length - 1
            return temp.data

    def top(self):
        # Return the data in the element at the beginning but does not remove it.
        # Return None if stack is empty.
        if (self.topitem is None):
            return None
        else:
            return self.topitem.data

    def __len__(self):
        # Return the number of elements in the stack
        return self.length


def sum_exists(n, p_list):
    # Returns True if n can be formed from p_list repeated
    # some arbitrary number of times.
    if (n == 0):
        return True

    if (n < p_list[0] or len(p_list) == 0):
        return False

    sum_stack = MyStack(n)
    # adder stack tracks index of of each adder
    adder_stack = MyStack(0)
    # i is the index of p_list
    i = 0

    while (True):
        
        current_adder = p_list[adder_stack.top()]

        while ((sum_stack.top() >= current_adder)):
            sum_stack.push(sum_stack.top() - current_adder)
            # keep track of the index of adder not the acutal adder
            adder_stack.push(adder_stack.top())
            if (sum_stack.top() == 0):
                return True

        # sum overflow so pop the top sum attempt, 
        # return false if stack is empty after pop
        if (sum_stack.pop() == n):
            return False
        adder_stack.pop()

        # pop if current sum reach end of list (all possible combo tried for current sum)
        while ((adder_stack.top() == (len(p_list) - 1))):
            if (sum_stack.pop() == n):
                return False
            adder_stack.pop()

        # move on to the next adder in the list for current sum
        current_i = adder_stack.pop()
        adder_stack.push(current_i + 1)

    
