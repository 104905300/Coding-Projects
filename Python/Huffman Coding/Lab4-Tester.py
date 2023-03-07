import random
import string
import re
#Module Imports
import sys
from importlib import import_module

def GenerateFreqs(size=10):
    if (size <= 0) :
        size = 1
    elif (size > 26):
        size = 26
        
    freqs = {}
    letters=string.ascii_letters[:-26] + " '"
    chars = []
    for i in range(size):
            char=random.choice(letters)
            letters = letters.replace(char,"")
            freqs[char]=random.randint(0,size*2)
            chars.append(char)
    
    return chars, freqs

def GenerateWord(chars, size):
    word=""
    for i in range(0, random.randint(size/2, size)):
        word += random.choice(chars)
    return word
    

def Test(lib, seed=123456, size=10, rounds=10, verbose=False ):
    if not lib:
        print("You need to include a testable library")
        return False
    random.seed(a=seed)
    
    flag = True
    # Known string test -> 0 or 1 for long branch irrelevant, but length with be the same
    freqs = {'a': 15, 'd': 9, 'e': 18, 'H': 10, 'l': 16, 'o': 7, 'W': 4, 'r': 11, 'z': 3, ' ': 20}
    s="Hello World"
    try:
        huff = lib.MyHuffman()
    except:
        if verbose:
            print("Error: Tree not creatable")
        flag = False
    if verbose:
        print(f"Building tree from {freqs}")
    try:
        huff.build(freqs)
    except:
        if verbose:
            print("Error: Frequecy building not completable")
        flag = False
    
    if verbose:
        print(f"Encoding string \"{s}\"")
    try:
            bs = huff.encode(s)
    except:
        if verbose:
            print("Error: Word not encodable")
        flag = False
    if verbose:
        print(f"Received \"{bs}\"")
    if len(bs) != 38:
        if verbose:
            print(f"Error: Huffman algorithm not compressing properly. Expected 38 bits and got {len(bs)} bits.")
        flag = False
    
    if verbose:
        print("Encoding test complete")
    yield flag
    
    flag = True
    
    if verbose:
        print(f"Decoding back to original")
    
    try:
        rs = huff.decode(bs)
    except:
        if verbose:
            print("Error: Bitstring not decodable")
        flag = False
    if rs != s:
        if verbose:
            print(f"Error: Decoding incorrect. Expected {s} but got {rs}")
        flag = False
    if verbose:
        print(f"Correctly received \"{rs}\" from decoding \"{bs}\" from encoding \"{s}\"")

    if verbose:
        print("Decoding test complete")
    yield flag

    flag = True	
    testTree = lib.MyHuffman()
    fromTest = {'1':4, '2':4, '3':4, '4':4, '5':4, '6':4}
    testTree.build(fromTest)
    st = testTree.encode("123456")
    if (3*6)/len(st) != 1.125 :
        if verbose:
            print("Error: Huffman encoding not minimal form.")
        flag = False
    if verbose:
        print("Minimal Encoding test complete")
    yield flag
    flag = True		
	
    avgComp = 0.0
    for i in range(rounds):
        [chars, freqs]=GenerateFreqs(size)
        if verbose:
            print()
            print("Round " + str(i+1))
            print ("Current frequencies are: " + str(freqs))
        if not freqs:
            return None
        
        try:
            huff = lib.MyHuffman()
        except:
            if verbose:
                print("Error: Tree not creatable")
            flag = False
        try:
            huff.build(freqs)
        except:
            if verbose:
                print("Error: Frequecy building not completable")
            flag = False
        
        words = {}
        
        for j in range(1, rounds+1):
            word = GenerateWord(chars, j*2)
            bitstring = ""
            try:
                bitstring = huff.encode(word)
            except:
                if verbose:
                    print("Error: Word not encodable")
                flag = False
            if not re.search("^[0,1]+$",bitstring):
                if verbose:
                    print("Encoded string does not contain only 0 or 1 : " + bitstring)
                flag = False
            words[word] = bitstring

        for word, bitstring in words.items():
            decrypted = ""
            try:
                decrypted = huff.decode(bitstring)
            except:
                if verbose:
                    print("Error: Word not decodable")
                flag = False
            #if verbose:
               # if j == rounds:
               #     print(f"{word} -> {bitstring} -> {decrypted}")
            if not(word == decrypted):
                if verbose:
                    print(f"Error: {decrypted} should be {word}")
                flag = False

        #Big test efficieny check
        charsSpread = ""
        for char,frequency in freqs.items():

           for i in range(0,frequency):
               charsSpread += char
        
        paragraph = ""
        for i in range(0,size*10):
            paragraph += random.choice(charsSpread)
        
        try:
            paragraphBitString = huff.encode(paragraph)
        except:
            if verbose:
                print("Error: Paragraph not encodable")
            flag = False

        if not re.search("^[0,1]+$",paragraphBitString):
            if verbose:
                print("Encoded paragraph does not contain only 0 or 1 : " +paragraphBitString)
            flag = False
        try:
            paragraphUncompressed = huff.decode(paragraphBitString)
        except:
            if verbose:
                print("Error: Paragraph not decodable")
            flag = False
        if id(paragraph) == id(paragraphUncompressed):
            if verbose:
                print(f"Error: Returned string is the same as original.")
            flag = False
            
        if not(paragraph == paragraphUncompressed):
            if verbose:
                print(f"Error: {decrypted} should be {word}")
            flag = False
            
        pSize = len(paragraph) * 8
        pBSSize = len(paragraphBitString)
        perc = (pBSSize/pSize) * 100
        avgComp += perc
        if verbose:
            print("Paragraph compression reduced size to " + "{:.1f}".format(perc) + "% of the original")

    if verbose:
        print("Paragraph Compression/Decompression complete.")
    yield flag

    flag = True
    avgComp /= rounds
    if avgComp > 65:
        if verbose:
            print(f"Error: Paragraph compression average too high. Expected under 65%, got "+"{:.1f}".format(perc)+ "%")
            flag = False
    if verbose:
        print("Paragraph Compression Complete")
    yield flag
    
if __name__ == "__main__":

    if len(sys.argv) < 2:
        name = "Lab4"
    else:
        name = sys.argv[1]
        if name.startswith(".\\"):
            name = name[2:]
        if name.endswith(".py"):
            name = name[:-3]
    module=import_module(name,package=__name__)
    print(f"Testing module {name} by {module.getName()}")
    score = 0
    for i in Test(module,seed=123456, size=3000, rounds=20, verbose=True):
        if i:
            score+=1
    print(f"Test result: {score}/5")
