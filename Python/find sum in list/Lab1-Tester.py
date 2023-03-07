#Testing imports
import random
import math
#Module Imports
import sys
from importlib import import_module
import time

#Valid Bias/Seed List pairs
#From Oracled Code
BIASES = [0.3, 0.333, 0.3666, 0.4]
SEEDS= [[2150, 5279, 5668, 5800, 8541, 16308],
    [2386, 5279, 5668, 5800, 8541, 16308],
    [177, 4099, 5279, 5668, 8541, 16308, 18714],
    [177, 4099, 13520]
    ]


#For Prime Weights
PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]
PSUM = sum(PRIMES)*1.0
PWEIGHTS = [PRIMES[i]/PSUM for i in range(len(PRIMES))]
PWEIGHTS.reverse()

def Test(lib, seed=0, size=10, verbose=False, bias = 0.3):
    random.seed(a = seed)
    for i in  range(0,size):
        flag = True    

        # PRIMING THE RNG DO NOT MODIFY
        # gen number
        num = random.randrange(2,300)
        # gen true/false
        flip = random.random()+bias
        flip = round(flip)
        flip = bool(flip)
        # gen getlist
        p_len = random.randrange(2,6)
        # gen prime list
        p_list = random.choices(PRIMES, weights = PWEIGHTS, k= p_len)
        p_list = list(set(p_list))
        p_list.sort()
        #DO NOT MODIFY ABOVE
        exists = False
        try:
            exists = lib.sum_exists(num, 0, p_list)
        except:
            if verbose:
                print(f"Error: sum_exsts failed.") 
            flag = False

        if exists != flip:
            if verbose:
                print("Error: sum_exists returns incorrect.")
            flag = False
        
        solution = []
    
        try:
            solution = lib.find_sum(num, 0, p_list, [])
        except:
            if verbose:
                print("Error: sum_exists failed.")
            flag = False
        if flip:
            if len(solution)>0:                
                if not set(solution).issubset(set(p_list)):
                    if verbose:
                        print("Error: Returned solution has unacceptable values.")
                    flag = False
                
                if not sum(solution) == num:
                    if verbose:
                        print("Error: Solution does not sum to correct value.")
                    flag = False
            else:
                if flip:
                    if verbose:
                        print("Error: Returned solution empty for solvable number.")
                    flag = False
        else:
            if solution is not None:
                if len(solution) > 0:
                    if verbose:
                        print("Error: Returned solution for impossible problem.")        
                    flag = False

        yield flag
        

if __name__ == "__main__":
    VERBOSE = True 
    if len(sys.argv) < 2:
        name="Lab1"
    else:
        name = sys.argv[1]
        if name.startswith(".\\"):
            name = name[2:]
        if name.endswith(".py"):
            name = name[:-3]
    module=import_module(name,package=__name__)
    print(f"Testing module {name} by {module.getName()}")
    score=0
    start = time.time()
    for i in Test(module,seed=5279, size=20, verbose=VERBOSE, bias = 0.3):
        if time.time() - start > 10:
            if VERBOSE:
                print("Error: Allowed time elapsed.")
            break
        if i:
            score+=0.5
        
    if score % 1 == 0:
        score = math.floor(score)
    print(f"Execution time: {round(time.time()-start, 5)} seconds.")
    print(f"Test result: {score}/10")