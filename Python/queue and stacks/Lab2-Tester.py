# Testing imports
import random

# Module Imports
import sys
from importlib import import_module
import time


def TestSE(lib, start, verbose=False, tests=None, timeout=5, break_after_error=False):
    tally = 0
    faults = 0
    for case in tests:
        num = case[0]
        p_list = case[1:-1]
        expected = case[-1]
        result = lib.sum_exists(num, p_list)

        if result == expected:
            tally += 1
        else:
            if verbose:
                print(f"Error for test case: {num}, {p_list}")
                print(f"Returned: {result}; Expected: {expected}")
            if break_after_error:
                break

            faults += 1
            if faults > 10000:
                if verbose:
                    print("sum_exists test failed. Too many errors")
                    return 0

        time_delta = time.time() - start
        if time_delta > timeout:
            if verbose:
                print("Error: Allowed time elapsed.")
            break

    se_score = round(tally / len(tests) * 5)
    return int(se_score)


def TestStack(lib, seed=0, size=10, verbose=False):
    if not lib:
        print("You need to include a testable library")
        return False

    random.seed(a=seed)

    flag = True

    try:
        stack = lib.MyStack()
        stack
    except:
        if verbose:
            print("Error: Stack initialization incomplete")
        flag = False

    try:
        stack.top()
    except:
        if verbose:
            print("Error: fail to handle calling top() on an empty stack")
        flag = False

    try:
        stack.pop()
    except:
        if verbose:
            print("Error: fail to handle popping an empty stack")
        flag = False

    yield flag

    r = []
    flag = True
    for j in range(size):
        n = random.randint(0, size)
        r.append(n)
        try:
            stack.push(n)
        except:
            if verbose:
                print("Error: Stack push incomplete.")
            flag = False

    try:
        int(len(stack))
    except:
        if verbose:
            print("Error: Stack __len__ method not returning integer")
        flag = False

    if flag:
        if (len(stack) != size):
            if verbose:
                print("Error: Stack size should be " + str(size) + " but is " + str(len(stack)))
            flag = False

    if verbose:
        if flag:
            print("Stack size test complete")
        else:
            print("Stack size test failed")
    yield flag

    s = ""
    if flag:
        for j in range(size):
            try:
                s = stack.pop()
            except:
                if verbose:
                    print("Error: Stack retrieval incomplete")
                flag = False
            if r[size - j - 1] != s:
                if verbose:
                    print("Error: Stack value should be " + str(r[size - j - 1]) + " but is " + str(s))
                flag = False

    if verbose:
        if flag:
            print("Stack value test complete")
        else:
            print("Stack value test failed")
    yield flag

    flag = True
    r = []
    if flag:
        for j in range(size):
            n = random.randint(0, size)
            r.append(n)
            stack.push(n)

        for j in range(size):
            try:
                s = stack.top()
                stack.pop()
            except:
                if verbose:
                    print("Error: Stack top() method test incomplete")
                flag = False
            if r[size - j - 1] != s:
                if verbose:
                    print("Error: Stack value should be " + str(r[size - j - 1]) + " but is " + str(s))
                flag = False
    if verbose:
        if flag:
            print("Stack top() method test complete")
        else:
            print("Stack top() method test failed")
    yield flag
    # End stress test

    flag = True

    m = random.randint(0, size)
    n = random.randint(0, size)
    o = random.randint(0, size)

    stack2 = None
    try:
        stack.push(m)
        stack2 = lib.MyStack(data=n)
        stack2.push(o)
    except:
        if verbose:
            print("Error: Stack operations incorrect")
        flag = False

    oS = None
    try:
        oS = stack2.pop()
        oS
        oS = stack2.pop()
        oS
    except:
        flag = False
    if (oS != n):
        if verbose:
            print(f"Error: Stack retrieval should be {n} but is {oS}")
        flag = False

    if (stack.pop() != m):
        if verbose:
            print("Error: Stack instancing incomplete.")
        flag = False

    if verbose:
        if flag:
            print("Object instantiation test complete")
        else:
            print("Object instantiation test failed")
    yield flag


if __name__ == "__main__":
    VERBOSE = True
    # set this to True if you want to break after getting an error
    # when testing sum_exists
    BREAK_AFTER_ERROR = True

    if len(sys.argv) < 2:
        name = "Lab2"
    else:
        name = sys.argv[1]
        if name.startswith(".\\"):
            name = name[2:]
        if name.endswith(".py"):
            name = name[:-3]
    module = import_module(name, package=__name__)

    input_tests = []
    with open("Lab2-Test-Inputs.txt", 'r') as inputs:
        lines = inputs.readlines()
        lines = [x.strip() for x in lines]
        for line in lines:
            input_tests.append([int(x) for x in line.split(", ")])
            if input_tests[-1][-1] == 1:
                input_tests[-1][-1] = True
            else:
                input_tests[-1][-1] = False

    print(f"Testing module {name} by {module.getName()}")
    score = 0
    print("\nTesting Stack Implementation")
    for i in TestStack(module, seed=77777, size=30000, verbose=True):
        if i:
            score += 1

    print(f"Stack implementation score: {score}/5")
    print("\nTesting iterative sum_exists")
    start = time.time()
    score += TestSE(module, start, verbose=VERBOSE, tests=input_tests, timeout=5, break_after_error=BREAK_AFTER_ERROR)

    print(f"Execution time: {round(time.time() - start, 5)} seconds.")
    print(f"\nTest result: {score}/10")
