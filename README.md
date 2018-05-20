# pytrees

A collections of python3 implementations of trees.

## Classes

### AVL Tree

AVL Tree. 
Balanced Binary Search Tree. Gurantee for balance.

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

### Interval Tree

Augmented data structure for checking overlaps of intervals. Gurantee for balance.

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

### Binary Search Tree

Simple implementation of Binary Search Tree. No gurantee for balance.


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

## Convention: 

- "key" and "val" are almost the same in this implementation. use term "key" for search and delete a particular node. use term "val" for other cases
