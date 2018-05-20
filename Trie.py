"""
Trie (Prefix-Tree). 

Prefix-tree. Useful for text search.

API: 

- insert(self, word)
- search(self, word)
- startsWith(self, prefix)
- findAllWordsStartsWith(self, prefix)
- buildFromList(cls, l)

Author: Yi Zhou
Date: May 20, 2018 
Reference: https://leetcode.com/problems/implement-trie-prefix-tree/description/
Reference: https://en.wikipedia.org/wiki/Trie
"""

class TrieNode:
    def __init__(self):
        self.word = ""
        self.children = {}
      
class Trie:
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.root=TrieNode()
        
    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        root = self.root
        for char in word:
            root = root.children.setdefault(char,TrieNode())
        root.word = word
        
    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node=self.root
        for char in word:
            if char not in node.children:
                return False
            node=node.children[char]
        if node.word:
            return True
        else:
            return False
        
    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        node=self.root
        for char in prefix:
            if char not in node.children:
                return False
            node=node.children[char]
        return True
    
    def findAllWordsStartsWith(self, prefix):
        """
        Returns all words in the trie that starts with the given prefix.
        :type prefix: str
        :rtype: list 
        """
        node=self.root
        for char in prefix:
            if char not in node.children:
                return []
            node=node.children[char]
        res = []
        self._dfsFind(node, res)
        return res
    
    def _dfsFind(self, node, res):
        if node.word:
            res.append(node.word)
        for char in node.children:
            self._dfsFind(node.children[char], res)

    
    @classmethod
    def buildFromList(cls, l):
        """
        return a Trie object from l.
        """
        T = Trie()
        for item in l:
            T.insert(item)
        return T

if __name__ == "__main__":
    print("[BEGIN]Test Implementation of Trie.")
    T = Trie()
    T.insert("hel")
    T.insert("hell")
    T.insert("hello")
    T.insert("wor")
    T.insert("worl")
    T.insert("world")
    T.insert("word")
    print("search wo",T.search("wo"))
    print("search wor",T.search("wor"))
    print("startsWith h",T.startsWith("h"))
    print("findAllWordsStartsWith w",T.findAllWordsStartsWith("w"))
    print("findAllWordsStartsWith worl",T.findAllWordsStartsWith("worl"))
    print("[END]Test Implementation of Trie")
