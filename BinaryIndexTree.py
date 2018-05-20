"""
Binary Index Tree.

A Fenwick tree or Binary Indexed Tree is a data structure that can efficiently update elements and calculate prefix sums in a table of numbers.

Time Complexity: update & prefixSum, O(logN)
Space Complexity: O(N)

API: 

- update(self,i,k)  --> update value k to index i
- prefixSum(self,i) --> sum up [index 0, index 1, ..., index i]
- preview(self) 
- getSize(self)
- buildFromList(cls, l)

Author: Yi Zhou
Date: May 20, 2018 
Reference: https://en.wikipedia.org/wiki/Fenwick_tree
"""


class BinaryIndexTree(object):

    @classmethod
    def buildFromList(cls, l):
        T = BinaryIndexTree()
        T.num = [0] * len(l)
        T.BIT = [0] * (len(l)+1)
        T.size = len(l)
        for i in range(len(l)):
            T.update(i,l[i])
        return T
        
    def _lastBit(self,k):
        return (-k)&k
    
    def _getParent(self,k):
        return k - self._lastBit(k)
    
    def _getNext(self,k):
        return k + self._lastBit(k)
    
    def update(self,i,k):
        """
        Update BIT when there's an update event: num[i] <- k
        """
        start = i + 1
        while start <= len(self.num):
            self.BIT[start] += k-self.num[i]
            start = self._getNext(start)
        self.num[i] = k
    
    def prefixSum(self,i):
        """
        return num[0] + ... + num[i]
        """
        assert i < len(self.num)
        start = i + 1
        pSum = 0
        while start > 0 and start <= len(self.num):
            pSum += self.BIT[start]
            start = self._getParent(start)
        return pSum
    
    def preview(self):
        return self.num

    def getSize(self):
        return self.size

if __name__ == "__main__":
    l = [0,1,2,3,4,5,6,7,8,9,10]
    BIT = BinaryIndexTree.buildFromList(l)
    SIZE = len(BIT.preview())
    print(BIT.preview())
    for i in range(SIZE):
        print(BIT.prefixSum(i))
    BIT.update(0,1)
    print(BIT.preview())
    for i in range(SIZE):
        print(BIT.prefixSum(i))
    BIT.update(SIZE-1,-46)
    print(BIT.preview())
    for i in range(SIZE):
        print(BIT.prefixSum(i))
    