"""
Interval Tree

Augmented data structure for checking overlap of intervals. Gurantee for balance.

Convention: 

- key, val should be length 2 list/tuple, which is a interval. The interval stored in each node will be transformed into tuple.
- "key" and "val" are almost the same in this implementation. use term "key" for search and delete a particular node. use term "val" for other cases
- input interval [L,R] should satisfy L < R

API: 

- queryOverlap(self, val)
- queryAllOverlaps(self, val)
- insert(self, val)
- delete(self, key)
- search(self, key)
- getDepth(self)
- preOrder(self)
- inOrder(self)
- postOrder(self)
- countNodes(self)
- buildFromList(cls, l)


Author: Yi Zhou
Date: May 19, 2018 
Reference: http://research.engineering.nyu.edu/~greg/algorithms/classnotes/interval-trees.pdf
Reference: https://en.wikipedia.org/wiki/Interval_tree
"""


from collections import deque
import random


class IntervalNode:
    def __init__(self, val):
        assert len(val) == 2
        assert val[0] <= val[1]
        val = tuple(val) 
        self.val = val
        self.parent = None
        self.left = None
        self.right = None 
        self.height = 0
        self.maxRight = val[1] # Augmented DataStructure: Store the max right value of the subtree rooted at this node

    def isLeaf(self):
        return (self.height == 0)
    
    def maxChildrenHeight(self):
        if self.left and self.right:
            return max(self.left.height, self.right.height)
        elif self.left and not self.right:
            return self.left.height
        elif not self.left and  self.right:
            return self.right.height
        else:
            return -1
    
    def balanceFactor(self):
        return (self.left.height if self.left else -1) - (self.right.height if self.right else -1)
    
    def __str__(self):
        return "IntervalNode("+ str(self.val)+ ", maxRight: %d )" % self.maxRight
    

class IntervalTree:
    def __init__(self):
        self.root = None
        self.rebalance_count = 0
        self.nodes_count = 0
    
    def setRoot(self, val):
        """
        Set the root value
        """
        self.root = IntervalNode(val)
    
    def countNodes(self):
        return self.nodes_count
    
    def queryOverlap(self, val):
        """
        val should be an input interval.
        return IntervalNode that overlaps with the input interval that we find first in the IntervalTree.
        if not found, return None
        """
        assert len(val) == 2
        assert val[1] >= val[0]
        val = tuple(val)
        return self._dfsQueryOverlap(self.root, val)
    
    def _dfsQueryOverlap(self, node, val):
        """
        Helper function for query.
        return the first interval we find in the subtree rooted at node.
        """
        if not node: return None 
        if self._isOverlap(node.val, val):
            return node.val
        else:
            L, R = val
            if R < node.val[0]:
                # Case1
                #  Right subtree can't overlap, search left
                # ----- val
                #        ------ node.val
                #        /    \
                #     ----    -----
                return self._dfsQueryOverlap(node.left, val)
            elif L > node.val[1]:
                z = node.left.maxRight if node.left else (-float("inf"))
                if z >= L:
                    # Case2
                    # Left subtree guranteed overlap
                    #               L-----R 
                    #        ------ node.val
                    #        /    
                    #     -----.......z   
                    return self._dfsQueryOverlap(node.left, val)
                else:
                    # Case3
                    # Left subtree no overlap, search right
                    #               L-----R 
                    #        ------ node.val
                    #        /    
                    #     -----..z  
                    return self._dfsQueryOverlap(node.right, val)
            return None
    
    def queryAllOverlaps(self, val):
        """
        find all the intervals in the interval tree.

        return a list of all intervals that overlap with val.
        """
        assert len(val) == 2
        assert val[1] >= val[0]
        val = tuple(val)
        res = []
        self._dfsFind(self.root, val, res)
        return res
    
    def _dfsFind(self, node, val, res):
        """
        it should be better then naive iterations.
        """
        if not node: return None 

        if self._isOverlap(node.val, val):
            res.append(node.val)
        
        L, R = val
        if R < node.val[0]:
            # Case1
            #  Right subtree can't overlap, search left
            # ----- val
            #        ------ node.val
            #        /    \
            #     ----    -----
            self._dfsFind(node.left, val, res)
        elif L > node.val[1]:
            z = node.left.maxRight if node.left else (-float("inf"))
            if z<L:
                # Case3
                # Left subtree no overlap, search right
                #               L-----R 
                #        ------ node.val
                #        /    
                #     -----..z  
                self._dfsFind(node.right, val, res)
        else:
            self._dfsFind(node.left, val, res)
            self._dfsFind(node.right, val, res)
        return None
                
    def _isOverlap(self, interval1, interval2):
        """
        check intervals
        """
        l = sorted([interval1, interval2])
        if l[1][0] <= l[0][1] : 
            return True
        else:
            return False
    
    def getDepth(self):
        """
        Get the max depth of the BST
        """
        if self.root:
            return self.root.height
        else:
            return -1
    
    def _findSmallest(self, start_node):
        assert (not start_node is None)
        node = start_node
        while node.left:
            node = node.left
        return node
    
    def _findBiggest(self, start_node):
        assert (not start_node is None)
        node = start_node
        while node.right:
            node = node.right
        return node 

    def insert(self, val):
        """
        insert a val into IntervalTree
        """
        assert len(val) == 2
        assert val[1] >= val[0]
        val = tuple(val)
        if self.root is None:
            self.setRoot(val)
        else:
            self._insertNode(self.root, val)
        self.nodes_count += 1
    
    def _insertNode(self, currentNode, val):
        """
        Helper function to insert a value into IntervalTree.
        """
        # first, update the currentNode
        currentNode.maxRight = max(currentNode.maxRight, val[1])

        node_to_rebalance = None
        if currentNode.val > val:
            if(currentNode.left):
                self._insertNode(currentNode.left, val)
            else:
                child_node = IntervalNode(val)
                currentNode.left = child_node
                child_node.parent = currentNode
                if currentNode.height == 0:
                    self._recomputeHeights(currentNode)
                    node = currentNode
                    while node:
                        if node.balanceFactor() in [-2 , 2]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
        else:
            if(currentNode.right):
                self._insertNode(currentNode.right, val)
            else:
                child_node = IntervalNode(val)
                currentNode.right = child_node
                child_node.parent = currentNode
                if currentNode.height == 0:
                    self._recomputeHeights(currentNode)
                    node = currentNode
                    while node:
                        if node.balanceFactor() in [-2 , 2]:
                            node_to_rebalance = node
                            break #we need the one that is furthest from the root
                        node = node.parent
        if node_to_rebalance:
            self._rebalance(node_to_rebalance)
    
    def _recomputeMaxRight(self, node):
        """
        update the maxRight of an IntervalNode.
        """
        max1 = -float("inf") if not node.left else node.left.maxRight
        max2 = -float("inf") if not node.right else node.right.maxRight
        node.maxRight = max(node.val[1], max1, max2)

    def _rebalance(self, node_to_rebalance):
        """
        rebalance and fix maxRight due to rotation
        """
        A = node_to_rebalance 
        F = A.parent #allowed to be NULL
        if A.balanceFactor() == -2:
            if A.right.balanceFactor() <= 0:
                """Rebalance, case RRC 
                [Original]:                   
                        F                         
                      /  \
                 SubTree  A
                           \                
                            B
                             \
                              C

                [After Rotation]:
                        F                         
                      /  \
                 SubTree  B
                         / \  
                        A   C
                """
                B = A.right
                C = B.right
                assert (not A is None and not B is None and not C is None)
                
                A.right = B.left
                if A.right:
                    A.right.parent = A
                B.left = A
                A.parent = B                                                               
                if F is None:                                                              
                   self.root = B 
                   self.root.parent = None                                                   
                else:                                                                        
                   if F.right == A:                                                          
                       F.right = B                                                                  
                   else:                                                                      
                       F.left = B                                                                   
                   B.parent = F 
                self._recomputeHeights(A) 
                self._recomputeHeights(B.parent)
                self._recomputeMaxRight(A)
                self._recomputeMaxRight(B)
            else:
                """Rebalance, case RLC 
                [Original]:                   
                        F                         
                      /  \
                 SubTree  A
                           \                
                            B
                           /
                          C

                [After Rotation]:
                        F                         
                      /  \
                 SubTree  C
                         / \  
                        A   B
                """
                B = A.right
                C = B.left
                assert (not A is None and not B is None and not C is None)                
                B.left = C.right
                if B.left:
                    B.left.parent = B
                A.right = C.left
                if A.right:
                    A.right.parent = A
                C.right = B
                B.parent = C                                                               
                C.left = A
                A.parent = C                                                             
                if F is None:                                                             
                    self.root = C
                    self.root.parent = None                                                    
                else:                                                                        
                    if F.right == A:                                                         
                        F.right = C                                                                                     
                    else:                                                                      
                        F.left = C
                    C.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B)
                self._recomputeMaxRight(A)
                self._recomputeMaxRight(B)
                self._recomputeMaxRight(C)
        else:
            assert(node_to_rebalance.balanceFactor() == +2)
            if node_to_rebalance.left.balanceFactor() >= 0:
                """Rebalance, case LLC 
                [Original]:                   
                        F                         
                      /  \
                     A   SubTree
                    /
                   B
                  /
                 C   

                [After Rotation]:
                        F                         
                       / \  
                      B  SubTree
                     / \  
                    C   A
                """
                B = A.left
                C = B.left
                assert (not A is None and not B is None and not C is None)
                A.left = B.right
                if A.left:
                    A.left.parent = A
                B.right = A
                A.parent = B                                                               
                if F is None:                                                              
                   self.root = B 
                   self.root.parent = None                                                   
                else:                                                                        
                   if F.right == A:                                                          
                       F.right = B                                                                  
                   else:                                                                      
                       F.left = B                                                                   
                   B.parent = F 
                self._recomputeHeights(A) 
                self._recomputeHeights(B.parent)
                self._recomputeMaxRight(A)
                self._recomputeMaxRight(B)
            else:
                """Rebalance, case LRC 
                [Original]:                   
                        F                         
                      /  \
                     A   SubTree
                    /
                   B
                    \
                     C
                   

                [After Rotation]:
                        F                         
                       / \  
                      C  SubTree
                     / \  
                    B   A
                """
                B = A.left
                C = B.right
                assert (not A is None and not B is None and not C is None)
                A.left = C.right
                if A.left:
                    A.left.parent = A
                B.right = C.left
                if B.right:
                    B.right.parent = B
                C.left = B
                B.parent = C
                C.right = A
                A.parent = C
                if F is None:
                   self.root = C
                   self.root.parent = None
                else:
                   if (F.right == A):
                       F.right = C
                   else:
                       F.left = C
                   C.parent = F
                self._recomputeHeights(A)
                self._recomputeHeights(B)
                self._recomputeMaxRight(A)
                self._recomputeMaxRight(B)
                self._recomputeMaxRight(C)
        self.rebalance_count += 1

    def _recomputeHeights(self, start_from_node):
        changed = True
        node = start_from_node
        while node and changed:
            old_height = node.height
            node.height = (node.maxChildrenHeight() + 1 if (node.right or node.left) else 0)
            changed = node.height != old_height
            node = node.parent
    
    def search(self, key):
        """
        Search a IntervalNode satisfies IntervalNode.val = key.
        if found return IntervalNode, else return None.
        """
        assert len(key) == 2
        assert key[1] >= key[0]
        key = tuple(key)
        return self._dfsSearch(self.root, key)
    
    def _dfsSearch(self, currentNode, key):
        """
        Helper function to search a key in IntervalTree.
        """
        if currentNode is None:
            return None
        elif currentNode.val == key:
            return currentNode
        elif currentNode.val > key:
            return self._dfsSearch(currentNode.left, key)
        else:
            return self._dfsSearch(currentNode.right, key)
    
    def delete(self, key):
        """
        Delete a key from IntervalTree
        """
        assert len(key) == 2
        assert key[1] >= key[0]
        key = tuple(key)

        # first find
        node = self.search(key)
        
        if not node is None:
            self.nodes_count -= 1
            #     There are three cases:
            # 
            #     1) The node is a leaf.  Remove it and return.
            # 
            #     2) The node is a branch (has only 1 child). Make the pointer to this node 
            #        point to the child of this node.
            # 
            #     3) The node has two children. Swap items with the successor
            #        of the node (the smallest item in its right subtree) and
            #        delete the successor from the right subtree of the node.
            if node.isLeaf():
                self._removeLeaf(node)
            elif (bool(node.left)) ^ (bool(node.right)):  
                self._removeBranch(node)
            else:
                assert (node.left) and (node.right)
                self._swapWithSuccessorAndRemove(node)

    def _removeLeaf(self, node):
        parent = node.parent
        if (parent):
            if parent.left == node:
                parent.left = None
            else:
                assert (parent.right == node)
                parent.right = None
            self._recomputeHeights(parent)
        else:
            self.root = None
        del node

        # recomputeMaxRight due to the deletion
        changed = True
        node = parent
        while node and changed:
            old_maxRight = node.maxRight
            self._recomputeMaxRight(node)
            changed = (node.maxRight != old_maxRight)
            node = node.parent

        # rebalance
        node = parent
        while (node):
            if not node.balanceFactor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent
        
    def _removeBranch(self, node):
        parent = node.parent
        if (parent):
            if parent.left == node:
                parent.left = node.right if node.right else node.left
            else:
                assert (parent.right == node)
                parent.right = node.right if node.right else node.left
            if node.left:
                node.left.parent = parent
            else:
                assert (node.right)
                node.right.parent = parent 
            self._recomputeHeights(parent)
        del node

        # recomputeMaxRight due to the deletion
        changed = True
        node = parent
        while node and changed:
            old_maxRight = node.maxRight
            self._recomputeMaxRight(node)
            changed = (node.maxRight != old_maxRight)
            node = node.parent

        # rebalance
        node = parent
        while (node):
            if not node.balanceFactor() in [-1, 0, 1]:
                self._rebalance(node)
            node = node.parent
    
    def _swapWithSuccessorAndRemove(self, node):
        successor = self._findSmallest(node.right)
        self._swapNodes(node, successor)
        assert (node.left is None)
        if node.height == 0:
            self._removeLeaf(node)
        else:
            self._removeBranch(node)
    
    def _swapNodes(self, node1, node2):
        assert (node1.height > node2.height)
        parent1 = node1.parent
        leftChild1 = node1.left
        rightChild1 = node1.right
        parent2 = node2.parent
        assert (not parent2 is None)
        assert (parent2.left == node2 or parent2 == node1)
        leftChild2 = node2.left
        assert (leftChild2 is None)
        rightChild2 = node2.right
        
        # swap heights
        tmp = node1.height 
        node1.height = node2.height
        node2.height = tmp
       
        if parent1:
            if parent1.left == node1:
                parent1.left = node2
            else:
                assert (parent1.right == node1)
                parent1.right = node2
            node2.parent = parent1
        else:
            self.root = node2
            node2.parent = None
            
        node2.left = leftChild1
        leftChild1.parent = node2
        node1.left = leftChild2 # None
        node1.right = rightChild2
        if rightChild2:
            rightChild2.parent = node1 
        if not (parent2 == node1):
            node2.right = rightChild1
            rightChild1.parent = node2
            parent2.left = node1
            node1.parent = parent2
        else:
            node2.right = node1
            node1.parent = node2
        
        # recomputeMaxRight due to the swap
        changed = True
        node = node2
        while node and changed:
            old_maxRight = node.maxRight
            self._recomputeMaxRight(node)
            changed = (node.maxRight != old_maxRight)
            node = node.parent

    def inOrder(self):
        res = []
        def _dfs_in_order(node, res):
            if not node:
                return
            _dfs_in_order(node.left,res)
            res.append(node.val)
            _dfs_in_order(node.right,res)
        _dfs_in_order(self.root, res)
        return res
    
    def preOrder(self):
        res = []
        def _dfs_pre_order(node, res):
            if not node:
                return
            res.append(node.val)
            _dfs_pre_order(node.left,res)
            _dfs_pre_order(node.right,res)
        _dfs_pre_order(self.root, res)
        return res
    
    def postOrder(self):
        res = []
        def _dfs_post_order(node, res):
            if not node:
                return
            _dfs_post_order(node.left,res)
            _dfs_post_order(node.right,res)
            res.append(node.val)
        _dfs_post_order(self.root, res)
        return res
    
    @classmethod
    def buildFromList(cls, l, shuffle = True):
        """
        return a IntervalTree object from l.
        suffle the list first for better balance.
        """
        if shuffle:
            random.seed()
            random.shuffle(l)
        IT = IntervalTree()
        for item in l:
            IT.insert(item)
        return IT
    
    def visulize(self):
        """
        Naive Visulization. 
        Warn: Only for simple test usage.
        """
        if self.root is None:
            print("EMPTY TREE.")
        else:
            print("-----------------Visualize Tree----------------------")
            layer = deque([self.root])
            layer_count = self.getDepth()
            while len( list(filter(lambda x:x is not None, layer) )):
                new_layer = deque([])
                val_list = []
                while len(layer):
                    node = layer.popleft()
                    if node is not None:
                        val_list.append((node.val,node.maxRight))
                    else:
                        val_list.append(" ")
                    if node is None:
                        new_layer.append(None)
                        new_layer.append(None)
                    else:
                        new_layer.append(node.left)
                        new_layer.append(node.right)
                val_list = [" "] * layer_count + val_list
                print(*val_list, sep="  ", end="\n")
                layer = new_layer
                layer_count -= 1
            print("-----------------End Visualization-------------------")

if __name__ == "__main__":
    print("[BEGIN]Test Implementation of IntervalTree.")
    # Simple Insert Test
    IT = IntervalTree()
    IT.insert((0,6))
    IT.insert((5,9))
    IT.insert((7,8))
    IT.insert((9,12))
    IT.insert((11,13))
    IT.insert((6,20))
    IT.insert((18,22))
    IT.visulize()
    # Simple Delete Test
    IT.delete((9,12))
    IT.visulize()
    IT.delete((5,9))
    IT.visulize()
    IT.delete((6,20))
    IT.visulize()
    IT.delete((0,6))
    IT.visulize()
    # Test queryOverlap
    intervals = [
        [7,10],
        [5,11],
        [4,8],
        [17,19],
        [15,18],
        [21,23]
    ]
    overlaps = IntervalTree.buildFromList(intervals)
    overlaps.visulize()
    print("Overlap with [20,22]",overlaps.queryOverlap([20,22]))
    print("Overlap with [24,25]",overlaps.queryOverlap([24,25]))
    print("After Insert [24,24]")
    overlaps.insert([24,24])
    print("Overlap with [24,25]",overlaps.queryOverlap([24,25]))
    print("Overlap with [5,9]",overlaps.queryOverlap([5,9]))
    print("Overlap with [16,17]",overlaps.queryOverlap([16,17]))
    print("After Delete [15,18]")
    overlaps.delete([15,18])
    print("Overlap with [16,17]",overlaps.queryOverlap([16,17]))
    print("Overlap with [0,3]",overlaps.queryOverlap([0,3]))
    # Test findAllOverlaps
    print("queryAllOverlaps with [10,20]",overlaps.queryAllOverlaps([10,20]))
    print("[END]Test Implementation of IntervalTree.")