"""
AVL Tree. 

Balanced Binary Search Tree. Gurantee for balance.

Convention: 

- "key" and "val" are almost the same in this implementation. use term "key" for search and delete a particular node. use term "val" for other cases

API: 

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
Reference: https://en.wikipedia.org/wiki/AVL_tree
Reference: https://github.com/pgrafov/python-avl-tree/blob/master/pyavltree.py
"""

from collections import deque
import random


class AVLNode:
    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None 
        self.height = 0

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
        return "AVLNode("+ str(self.val)+ ", Height: %d )" % self.height

class AVLTree:
    def __init__(self):
        self.root = None
        self.rebalance_count = 0
        self.nodes_count = 0
    
    def setRoot(self, val):
        """
        Set the root value
        """
        self.root = AVLNode(val)
    
    def countNodes(self):
        return self.nodes_count
    
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
        insert a val into AVLTree
        """
        if self.root is None:
            self.setRoot(val)
        else:
            self._insertNode(self.root, val)
        self.nodes_count += 1
    
    def _insertNode(self, currentNode, val):
        """
        Helper function to insert a value into AVLTree.
        """
        node_to_rebalance = None
        if currentNode.val > val:
            if(currentNode.left):
                self._insertNode(currentNode.left, val)
            else:
                child_node = AVLNode(val)
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
                child_node = AVLNode(val)
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

    def _rebalance(self, node_to_rebalance):
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
        Search a AVLNode satisfies AVLNode.val = key.
        if found return AVLNode, else return None.
        """
        return self._dfsSearch(self.root, key)
    
    def _dfsSearch(self, currentNode, key):
        """
        Helper function to search a key in AVLTree.
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
        Delete a key from AVLTree
        """
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
        return a AVLTree object from l.
        suffle the list first for better balance.
        """
        if shuffle:
            random.seed()
            random.shuffle(l)
        AVL = AVLTree()
        for item in l:
            AVL.insert(item)
        return AVL
    
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
                        val_list.append(node.val)
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
    print("[BEGIN]Test Implementation of AVLTree.")
    # Simple Insert Test
    AVL = AVLTree()
    AVL.insert(0)
    AVL.insert(1)
    AVL.insert(2)
    AVL.insert(3)
    AVL.insert(4)
    AVL.insert(5)
    AVL.insert(6)
    AVL.insert(7)
    AVL.insert(8)
    AVL.insert(9)
    AVL.insert(10)
    AVL.insert(11)
    AVL.insert(12)
    AVL.insert(13)
    AVL.insert(14)
    print("Total nodes: ",AVL.nodes_count)
    print("Total rebalance: ",AVL.rebalance_count)
    # Simple Delete Test
    AVL.visulize()
    AVL.delete(2)
    AVL.visulize()
    AVL.delete(5)
    AVL.visulize()
    AVL.delete(6)
    AVL.visulize()
    AVL.delete(4)
    AVL.visulize()
    AVL.delete(0)
    AVL.visulize()
    AVL.delete(3)
    AVL.visulize()
    AVL.delete(1)
    AVL.delete(7)
    AVL.delete(8)
    AVL.delete(9)
    AVL.visulize()
    AVL.delete(10)
    AVL.delete(12)
    AVL.visulize()
    print("Total nodes: ",AVL.nodes_count)
    print("Total rebalance: ",AVL.rebalance_count)
    print("----------------------------------------")
    input_list = list(range(2**16))
    new_AVL = AVLTree.buildFromList(input_list,shuffle = False)
    print("Total Nodes:",new_AVL.countNodes())
    print("Total Depth:",new_AVL.getDepth())
    print("Total rebalance: ",new_AVL.rebalance_count)
    new_AVL = AVLTree.buildFromList(input_list,shuffle = True)
    print("Total Nodes:",new_AVL.countNodes())
    print("Total Depth:",new_AVL.getDepth())
    print("Total rebalance: ",new_AVL.rebalance_count)
    print("Test inOrder:",  new_AVL.inOrder()==list(range(2**16)))
    print("[END]Test Implementation of AVLTree.")
