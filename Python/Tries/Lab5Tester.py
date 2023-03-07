#   Tester for CCPS305 Lab 5
#   You will need the 'american-english-no-accents' file in the directory of the tester



from enum import Flag
import random
import string
import re
#Module Imports
import string
import sys
from importlib import import_module

wordlist = []
def prepare():
    global wordlist
    try:
        f = open("american-english-no-accents.txt", "r")
    except:
        print("Error: Please ensure the wordlist file is in this directory.")
        exit()
    readwords = f.readlines()
    for word in readwords:
        wordlist.append(word.rstrip())

def GenerateWord(size):
    chars=string.ascii_letters+"'"
    word=""
    for i in range(0, random.randint(size/2, size)):
        word += random.choice(chars)
    return word

def diff(li1, li2):
    return (list(list(set(li1)-set(li2)) + list(set(li2)-set(li1))))     

def Test(lib, seed=0, size=10, verbose=False, wordlist=wordlist):
    wordlist = wordlist.copy()
    random.seed(a=seed)
    rounds = size
    if not lib:
        print("You need to include a testable library")
        return False

    # ORD FUNCTIONALITY TEST
    # flag = True
    # try:
    #     if lib.MyTrie.char_to_position("c") != 29 or lib.MyTrie.char_to_position("J") != 10:
    #         verbose and print ("Error: char_to_position incorrect.")
    #         flag = False
    # except:
    #     verbose and print("Error: char_to_position nonfunctional.")
    #     flag = False
    # verbose and print("Ord Functionality test " +("complete." if flag else "failed."))
    # yield flag

    # SMALL TEST
    flag = True
    try:
        trie = lib.MyTrie()
    except:
        verbose and print("Error: Cannot create Trie.")
        return False

    try:
        trie.insert("Apple")
        trie.insert("Adam")
        trie.insert("alpha")
    except:
        verbose and print("Errror: Trie insertion fails.")
        flag = False
    
    # try:
    #     if len(trie) != 3:
    #         verbose and print("Error: Child count incorrect.")
    #         flag = False
    # except:
    #     verbose and print("Error: len function uncallable.")
    #     flag = False

    try:
        if trie.depth_of_word("Apple") != 2 or trie.depth_of_word("alpha") != 1:
            verbose and print("Error: Word depth incorrect.")
            flag = False
    except:
        verbose and print("Error: depth_of_word fails.")
    
    verbose and print("Small Trie test " +("complete." if flag else "failed."))
    yield flag
    del(trie)

    # INSERTION TEST
    flag = True
    try:
        trie = lib.MyTrie()
    except:
        verbose and print("Error: Cannot recreate Trie.")
        return False

    for word in wordlist:
        try:
            trie.insert(word)
        except:
            verbose and print(f"Error: Failed to insert {word} into trie.")
            flag = False

    # if len(wordlist) != len(trie):
    #     if verbose:
    #         print("Trie size mismatch!")
    #     flag = False

    if verbose:
        print("Insertion test " + ("complete." if flag else "failed."))
    yield flag

    # EXISTS CHECK
    for j in range(0, rounds):
        expected = True
        c=""

        if random.randint(0,2) == 0:
            c = GenerateWord(6)
        else:
            c = wordlist[random.randint(0, len(wordlist))]
        expected = c in wordlist
        res = trie.exists(c)
        if res != expected:
            if verbose:
                print("Word " + c + " was " + ("found" if res else "not found") + " and was expected to " + ("" if expected else "not") + " be.")
            flag = False
            break
    if verbose:
        print("Trie item test " + ("complete." if flag else "failed."))
    yield flag

    # EMPTY PREFIX TEST
    try:
        mlist = trie.autoComplete("")
    except:
        if verbose:
            print("Error: Autocomplete method not callable")
        return False

    if not(set(mlist) == set(wordlist)):
        if verbose:
            missing = diff(mlist, wordlist)
            missing.sort()
            print(f"Error: Autocomplete missing {len(missing)}/{len(wordlist)} items for empty prefix")
            #print(missing)
        return False
    
    if verbose:
        print("Complete retrieval test complete")
    yield True

    # REMOVE TEST
    flag = True
    remlist = []
    for _ in range(0, rounds*5):

        w = random.choice(list(set(wordlist)-set(remlist)))
        
        try:
            trie.remove(w)
            assert not trie.exists(w)
            remlist.append(w)
            
        except:
            verbose and print("Error: Cannot remove item from trie.")
            flag = False
            break

    verbose and print("Removal test "+ ("complete." if flag else "failed."))
    yield flag
    yield flag

    # # REMOVAL LENGTH UPDATE
    # flag = True
    # if len(trie) != len(list(set(wordlist)-set(remlist))):
    #     verbose and print("Error: Length incorrect after removal")
    #     flag = False
    # verbose and print("Removal length update test "+ ("complete." if flag else "failed."))
    # yield flag

    # REMOVAL EMPTY PREFIX TEST
    try:
        mlist = trie.autoComplete("")
        if set(mlist) != set(wordlist)-set(remlist):
            verbose and print("Error: Autocomplete including removed items.")
    except:
        verbose and print("Error: autoComplete not working after removal.")
        flag = False
    yield flag


    # INVALID PREFIX TEST
    flag = True
    try:
        emptyList = trie.autoComplete("fasdfasdfasdfasfawef")
    except:
        if verbose:
            print("Error: Autocomplete does not respond to unmatched prefix")
        flag = False
    
    if len(emptyList) != 0:
        if verbose:
            print("Error: Autocomplete returning items for unmatchable prefix")
        flag = False

    if verbose:
        print("Unmatchable prefix test " + ("complete." if flag else "failed."))
    yield flag
    

    # Reinserting
    for x in remlist:
        try:
            trie.insert(x)
            assert trie.exists(x)
        except:
            verbose and print("Error: Cannot reinsert removed item into trie")
            flag = False
            break


    # COMPLETE AUTOCOMPLETE TEST
    for _ in range(0,rounds):
        w = ""
        while len(w) < 4:
            w = random.choice(wordlist)
        prefix =  w[0:3]
        matchlist = list(filter(lambda x: x.startswith(prefix), wordlist))
        try:
            autocompletelist = trie.autoComplete(prefix)
        except:
            if verbose:
                print("Error: Autocomplete method not callable")
            return False
        sMatch = set(matchlist)
        sAuto = set(autocompletelist)
        if not (sMatch == sAuto): # Check more problems? ie not in order, in order but missing, etc
            if verbose:
                # print(f"Expected: {matchlist}")
                # print(f"Output  : {autocompletelist}")
                if sAuto < sMatch:
                    print("Error: Autocomplete method not returning all matching items.")
                elif sMatch == sAuto:
                    print("Error: Autocomplete order incorrect.")
                elif sMatch < sAuto:
                    print("Error: Autocomplete returning extra items.")
                else:
                    print("Error: Autocomplete returning incorrect items.")
            flag = False

            break

    if verbose:
        print("Full Autocomplete test " + ("complete." if flag else "failed."))
    yield flag
    yield flag

    


if __name__ == "__main__":
    if len(sys.argv) < 2:
        name="Lab5"
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
    for i in Test(module,seed=123456, size=20, verbose=True):
        if i:
            score+=1
    print(f"Test result: {score}/10")
