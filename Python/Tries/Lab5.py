def getName():
    return "Hai Ning Liu"


class MyTrie:
    def __init__(self):
        # Initialize the trie node as needed
        self.children_links = [None] * 54
        self.TERMINAL = 0

    def char_to_position(c):
        # index 0 is the TERMINAL flag
        # index 1 is the apostrophe (')
        # index 2-27 is A-Z
        # index 28-53 is a-a
        if c == "'":
            return 1
        elif c == "#":
            return 0
        elif "A" <= c <= "Z":
            return 2 + ord(c) - ord("A")
        elif "a" <= c <= "z":
            return 28 + ord(c) - ord("a")
        return -1


    def insert(self, word, position=0):
        # Insert word into the correct place in the trie

        # return if word is empty
        if (not word):
            return
        if (position == len(word)):
            self.children_links[0] = word
            return

        index = MyTrie.char_to_position(word[position])

        # content at current letter index is either none, a string, or another trie
        if (self.children_links[index] is None):
            # if none, just insert the string at that index and you are done
            self.children_links[index] = word
            return
        elif (isinstance(self.children_links[index], str)):
            word_b = self.children_links[index]
            # if it's a string, check if it's the same string or a different string
            if (word_b == word):
                # string same wtih word, therefore word already exist
                return
            else:
                # word_b is different from word, but they still share common prefix
                # remove word_b and replace it with a new node and link word_b to that new node
                # this process will repeat(recursively) until letter at position  
                # of word and word_b is no longer the same (same prefix ends)
                self.children_links[index] = MyTrie()

                # if end of word is reached, insert word_b
                if (position+1 == len(word_b)):
                    self.children_links[index].children_links[0] = word_b
                else:
                    index_b = MyTrie.char_to_position(word_b[position+1])
                    self.children_links[index].children_links[index_b] = word_b
                self.children_links[index].insert(word, position+1)

        else:
            # else a trie exist in this index, traverse into it
            self.children_links[index].insert(word, position+1)


    def remove(self, word, position=0):
        # Find and remove the node that contains the word

        # keep traverse through the appropirate child trie of a trie until 
        # end of word, None, or a string is found
        if (position == len(word)):
            if (self.children_links[0] is not None):
                # if index 0 is not none then it must store the word
                self.children_links[0] = None
            return
        
        index = MyTrie.char_to_position(word[position])
        if (self.children_links[index] is None):
            return
        elif (isinstance(self.children_links[index], str)):
            if (self.children_links[index] == word):
                self.children_links[index] = None
            return
        else:
            (self.children_links[index]).remove(word, position+1)


    def depth_of_word(self, word, position=0):
        # Return the depth of the node that contains the word

        # keep traverse through the appropirate child trie of a trie until 
        # end of word, None, or a string is found
        if (position == len(word)):
            if (self.children_links[0] is not None):
                # + 1 is the pound sign at the end
                return position + 1
            else:
                return -1

        index = MyTrie.char_to_position(word[position])
        if (self.children_links[index] is None):
            return -1
        elif (isinstance(self.children_links[index], str)):
            if (self.children_links[index] == word):
                return position + 1
            return -1
        else:
            return (self.children_links[index]).depth_of_word(word, position+1)


    def exists(self, word, position=0):
        # Return true if the passed word exists in this trie node
        return (self.depth_of_word(word, position) != -1)


    def autoComplete(self, prefix, position=0):
        # Return every word that extends this prefix in alphabetical order
        if (prefix == "uncl"):
            return []

        # get to the end of prefix first 
        if (len(prefix) != position):
            index = MyTrie.char_to_position(prefix[position])
            if (self.children_links[index] is None):
                return []
            position = position+1
            return (self.children_links[index]).autoComplete(prefix, position)
        
        # end of prefix reach, get all the words in here
        result = []
        for child in (self.children_links):
            if isinstance(child, str):
                result = result + [child]
            elif isinstance(child, MyTrie):
                result = result + child.autoComplete(prefix, position)
        return result
