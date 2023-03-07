
import time
import math
import random
#Module Imports
import sys
from importlib import import_module

def prepare():
    return True

def CheckHeight(tree):
    if tree is None:
        return -1
    else:
        return max(CheckHeight(tree.getLeft())+1,CheckHeight(tree.getRight())+1)

def CheckBST(tree):
    flag = True
    if tree.getLeft() is not None:
        if tree.getData() <= tree.getLeft().getData():
            return False
        else:
            flag = flag and CheckBST(tree.getLeft())
    if tree.getRight() is not None:
        if tree.getData() > tree.getRight().getData():
            return False
        else:
            flag = flag and CheckBST(tree.getRight())
    return flag
    

def CheckAVL(tree):
    if  CheckHeight(tree) > 0:
        l = 0 if tree.getLeft() is None else CheckHeight(tree.getLeft())+1
        r = 0 if tree.getRight() is None else CheckHeight(tree.getRight())+1
        b = l-r
        if abs(b) >= 2 or b != tree.getBalanceFactor():
            print(f"balance factor is {b} and tree claims it is {tree.getBalanceFactor()}")
            printTree(tree)
            return False
        else:
            return CheckAVL(tree.getLeft()) and CheckAVL(tree.getRight())
    else:
        return True

def printTree_(tree, prefix):
    if tree.getLeft() is not None:
        printTree_(tree.getLeft(),prefix+"+ ")
    print(f"{prefix}{tree.data}")
    if tree.getRight() is not None:
        printTree_(tree.getRight(),prefix+"- ")

def printTree(tree):
    printTree_(tree,"")

def Test(lib, seed=0, size=10, rounds=10, verbose=False):
    random.seed(a=seed)
    # Test MyTree
    flag = True
    n = random.randint(0, size)
    
    flag = True
    m = size*3
    n = random.randint(size, size*2)

    try:
        bst = lib.MyBST(n)
        for i in range(1,5):
            bst.insert(n+i)
        bst = bst.insert(n-2)
        bst = bst.insert(n-1)
    except:
        if verbose:
            print("Error: MyBST not creatable")
        flag = False

    if bst.getHeight() != 4 or bst.getHeight() != CheckHeight(bst):
        if verbose:
            print("Error: BST height incorrect.")
        flag = False

    if verbose:
        if flag:
            print("BST getHeight() test complete.")
        else:
            print("BST getHeight() test failed.")
    del(bst)
    yield flag

    flag = True
    bst= lib.MyBST(n)
    a = [n]
    a_all = [n]
    for i in range(size):
        v = random.randint(0,m)
        bst= bst.insert(v)
        a_all.append(v)
        if not(v in a):
            a.append(v)
        
    for i in range(size):
        if len(a) >= size:
            m*=2
        v = random.randint(0,m)
        if (v in a) != (v in bst):
            if verbose:
                print("Error: BST Search incorrect")
            flag = False
    if verbose:
        if flag:
            print("BST search test complete.")
        else:
            print("BST search test failed.")
    yield flag

    flag = True
    # copy Small/Large test
    minVal = min(a)
    maxVal = max(a)

    try:
        minTree = bst.findSmallest()
        if minVal != minTree:
            verbose and print(f"Error: BST returns minimum value as {minTree} when it should be {minVal}.")
            flag = False
    except:
        verbose and print("Error: findSmallest() does not work.")
        flag = False

    try:
        maxTree = bst.findLargest()
        if maxVal != maxTree:
            verbose and print(f"Error: BST returns minimum value as {maxTree} when it should be {maxVal}.")
            flag = False
    except:
        verbose and print("Error: findLargest() does not work.")
        flag = False

    if flag:
        verbose and print("BST findSmallest and findLargest test complete.")
    else:
        verbose and print("BST findSmallest and findLargest test failed.")   
    
    flag = True
    #Remove test
    #tiny
    smol_bst = lib.MyBST(4)
    smol_bst = smol_bst.insert(2)
    smol_bst = smol_bst.insert(3)
    smol_bst = smol_bst.insert(6)
    smol_bst = smol_bst.insert(5)
    try:
        if smol_bst.getHeight() != 2:
            flag = False
        else:
            smol_bst = smol_bst.remove(4)
            if (smol_bst.promote_right and smol_bst.data != 5) or ((not smol_bst.promote_right) and smol_bst.data != 3):
                verbose and print("Error: Remove promoting incorrect value.")
                flag = False
            else:
                if not CheckBST(smol_bst):
                    verbose and print("Error: Tree no longer a BST after removal.")
                    flag = False
            
    except:
        verbose and print("Error: BST Remove non-functional")
        flag = False
    #tiny complete
    del(smol_bst)

    if flag:
        verbose and print("BST Small Removal test complete.")
    else:
        verbose and print("BST Small Removal test failed.")
    
    if flag:
        try:
            random.shuffle(a)
            d = []
            for v in a:
                for i in range(a_all.count(v)):
                    d.append(v)
            v = d[0]
            for val in d[:-1]:
                bst = bst.remove(val)
                if val != v:
                    if v in bst:
                        verbose and print(f"Error: BST Removal not removing values. {v} still in tree after removing all instances.")
                        flag = False
                    v = val            
            if bst.getData() != d[-1]:
                verbose and print("Error: BST removal not promoting correct values.")
                flag = False
        

        except:
            verbose and print("Error: large BST removal uncompletable.")
            flag = False

        if flag:
            verbose and print("BST Large Removal test complete.")
        else:        
            verbose and print("BST Large Removal test failed.")
        yield flag

    else:
        verbose and print("Skipping large BST removal test.")
        yield flag
    

    
    flag = True

    n=10
    try:
        avl = lib.MyAVL(n)
        first = avl
        avl = avl.insert(n+6)
        avl = avl.insert(n+12)
    except:
        if verbose:
            print("Error: MyAVL not creatable")
        flag = False
    try:
        if not(first is avl.getLeft()):
            if verbose:
                print("Error: AVL Rotation incorrect #1")
            flag = False
    except:
        verbose and print("Error: Node lost after insertion.")
        flag = False

    try:
        second = avl.getRight()
        second
    except:
        if verbose:
            print("Error: AVL Node lost during rotation")
        flag = False

    try:
        avl=avl.insert(8)
        avl=avl.insert(6)
    except:
        if verbose:
            print("Error: AVL Node not insertable")
        flag = False
    try:
        if not(first is avl.getLeft().getRight()):
            if verbose:
                print("Error: AVL Rotation incorrect #2")
            flag = False
    except:
        verbose and print("Error: Node lost after insertion.")
        flag = False
    
    if verbose:
        if flag:
            print("AVL Single Rotation test complete.")
        else:
            print("AVL Single Rotation test failed.")
    
    yield flag # Simple rotation correct

    flag = True
    try:
        avl=avl.insert(n-3)
    except:
        if verbose:
            print("Error: AVL Node not insertable")
        flag = False

    # Force rotations
    try:
        avl = avl.insert(n-2)
        avl = avl.insert(n-1)
        avl = avl.insert(n*2+4)
        avl = avl.insert(n*2+3)
    
        if not (first is avl.getRight().getLeft().getRight()):
            if verbose:
                print("Error: AVL Rotation incorrect #3")
            flag = False
    except:
        verbose and print("Error: Nodes lost after AVL insertion.")
        flag = False
    
    if verbose:
        if flag:
            print("AVL Double Rotation test complete.")
        else:
            print("AVL Double Rotation test failed.")
    yield flag # Rotation test complete

    flag = True
    try:
        for i in range(0, size):
            avl = avl.insert(random.randint(0,size))
    except:
        verbose and print("Error: Nodes lost after AVL insertion.")
        flag = False

    if not CheckAVL(avl):
        if verbose:
            print("Error: AVL Property not maintained across inserts")
        flag = False
    if verbose:
        if flag:
            print("AVL Property test complete.")
        else:
            print("AVL Property test failed.")
    yield flag # Big test complete
    
    verbose and print("\nBeginning AVL Large Removal test.")

    failedTrees = 0
    forest = size*10
    try:
        for i in range(forest):
            flag = True
            d = random.sample(range(10000), random.randint(20,100))
            #Inserting
            avl = lib.MyAVL(d[0])
            for j in d[1:]:
                avl = avl.insert(j)
                flag = flag and CheckAVL(avl)
                if not flag:
                    verbose and print("Error: AVL property lost during large insertion.")
            #Finding
            for j in d:
                f = j in avl
                if not f:
                    print(f"Error: Value {j} not inserted into tree.")
                flag = flag and f

            #Removing
            d_s = random.sample(d,random.randint(math.floor(len(d)/4), len(d)-1))
            for j in d_s:
                try:
                    avl=avl.remove(j)
                except:
                    verbose and print(f"Error: Cannot remove value {j}.")
                flag = flag and CheckAVL(avl)

            for j in d_s:
                f = j not in avl
                if not f:
                    verbose and print(f"Error: Value {j} remains in tree after removal.")
                flag = flag and f

            d_r = [item for item in d if item not in d_s]
            random.shuffle(d_r)
            for j in d_r:
                f = j in avl
                if not f:
                    verbose and print(f"Error: Value {j} missing from tree.")
                flag = flag and f

            if not flag:
                failedTrees += 1
    except:
        verbose and print("Error: AVL functionality broken.")
        return False

    if failedTrees > 1:
        verbose and print(f"Failed {failedTrees}/{forest}.\n")
        if failedTrees <= 20:
            verbose and print("AVL Large Removal test partially complete.")
        else:
            verbose and print("AVL Large Revoval test failed.")
    else:
        verbose and print("All trees correct.\n")
        verbose and print("AVL Large Removal test complete.")

    if failedTrees <= forest*0.2:
        yield True
    else:
        yield False
    if failedTrees <= forest*0.1:
        yield True
    else:
        yield False
    if failedTrees <= forest*0.05:
        yield True
    else:
        yield False
    if failedTrees == 0:
        yield True
    else:
        yield False

    
        



    
    
    
if __name__ == "__main__":
    VERBOSE = True 
    if len(sys.argv) < 2:
        name="Lab3"
    else:
        name = sys.argv[1]
        if name.startswith(".\\"):
            name = name[2:]
        if name.endswith(".py"):
            name = name[:-3]
    module=import_module(name,package=__name__)

    prepare()

    print(f"Testing module {name} by {module.getName()}")
    score=0
    start = time.time()
    for i in Test(module,seed=987456321, size=20, verbose=VERBOSE):
        if time.time() - start > 10:
            VERBOSE and print("Error: Allowed time elapsed.")
            break
        if i:
            score+=1
        
    if score % 1 == 0:
        score = math.floor(score)
    print(f"Execution time: {round(time.time()-start, 5)} seconds.")
    print(f"Test result: {score}/10")
