# username - complete info
# id1      - complete info
# name1    - complete info
# id2      - 204327258
# name2    - elhadperl

import random


class AVLNode(object):
    """Constructor, you are allowed to add more fields.

    @type value: str
    @param value: data of your node
    """

    def __init__(self, value, height=0, size=1):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None
        self.height = height
        self.size = size

    """returns the left child
    @rtype: AVLNode
    @returns: the left child of self, None if there is no left child
    time complexity : O(1)
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    time complexity : O(1)
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    time complexity : O(1)
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    time complexity : O(1)
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    time complexity : O(1)
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    time complexity : O(1)
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    time complexity : O(1)
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    time complexity : O(1)
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    time complexity : O(1)
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    time complexity : O(1)
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    time complexity : O(1)
    """

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    """returns the size of the node
           @rtype: int
           @returns: int if not-empty, 0 if empty
           time complexity : O(1)"""
    def getSize(self):
        return self.size

    """sets the size of the node
       @type s: int
       @pre: 0 <= i
       @param s: new size of node
       time complexity : O(1)"""
    def setSize(self, s):
        self.size = s

    """ calculates the Balance Factor of node
     @rtype: int
     @returns: the balance factor of node
     time complexity : O(1)"""
    def BFcalc(self):
        return (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(self)

    """ updates the height of node
    time complexity : O(1)"""
    def hUpdate(self):
        return (lambda n: max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)(self)

    """ updates the size of node
    time complexity : O(1)s"""
    def sUpdate(self):
        return (lambda n: n.getRight().getSize() + n.getLeft().getSize() + 1)(self)
"""
A class implementing the ADT list, using an AVL tree.
"""


class AVLTreeList(object):
    """
    Constructor, you are allowed to add more fields.

    """

    def __init__(self):
        self.root = None
        self.size = 0
        self.firstItem = None
        self.lastItem = None

    """returns whether the list is empty

    @rtype: bool
    @returns: True if the list is empty, False otherwise
    time complexity: O(1)v
    """

    def empty(self):
        if self.length() == 0:
            return True
        return False

    """retrieves the value of the i'th item in the list

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: index in the list
    @rtype: str
    @returns: the the value of the i'th item in the list
    """

    def retrieve(self, i):
        if i < 0 or i >= self.getSize():
            return None
        return self.retrieve_rec(self.getRoot(), i + 1).value
    """ actual retrieve function, """
    def retrieve_rec(self, node, i, printNodes=False, counter=1):
        rank = node.getLeft().getSize() + 1
        if rank == i:
            return node
        if i < rank:
            return self.retrieve_rec(node.getLeft(), i, printNodes, counter)
        else:
            return self.retrieve_rec(node.getRight(), i - rank,printNodes,counter)



    def append(self, val):
        return self.insert(self.length(), val)

    """inserts val at position i in the list

       @type i: int
       @pre: 0 <= i <= self.length()
       @param i: The intended index in the list to which we insert val
       @type val: str
       @param val: the value we inserts
       @rtype: list
       @returns: the number of rebalancing operation due to AVL rebalancing
       """
    def insert(self, i, val):
        elem = self.initNode(val)             # Initial new node
        if self.empty():                      # Empty list
            self.setRoot(elem), self.setFirst(elem), self.setLast(elem), self.setSize(self.getSize()+1)
            return 0

        if i == self.length():                  # i == len(lst)
            pos = self.appendNode(elem)
        else:
            pos = self.setNode(elem, i)    # Select(self, i+1) == self[i] ==> find the node located in index i
        elem.setParent(pos)
        self.size += 1
        return self.fixUp(pos) + 1

    """ create a new Node with Value val
       @type val: data
       @rtype: AVLNode
       @returns: new AVLNode"""


    def initNode(self, val):
        elem = AVLNode(val)
        vrNodeR = AVLNode(None, -1, 0)
        vrNodeL = AVLNode(None, -1, 0)
        elem.setRight(vrNodeR)
        elem.setLeft(vrNodeL)
        vrNodeR.setParent(elem)
        vrNodeL.setParent(elem)
        return elem

    """appends a new Node to the list
       @type elem: AVLNode
       @rtype: AVLNode
       @returns: the new parent of elem"""
    def appendNode(self, elem):
        pos = self.root
        while pos.getRight().getHeight() != -1:
            pos = pos.right
        pos.setRight(elem)
        self.setLast(elem)
        return pos

    """ sets a new node at index i
       @type elem: AVLNode
       @type i: int
       @pre: 0 <= i < self.length() 
       @rtype: AVLNode
       @returns: the new parent of elem"""
    def setNode(self, elem, i):
        pos = self.retrieve_rec(self.root, i + 1)
        if not pos.left.isRealNode():  # if pos.left is vr
            pos.setLeft(elem)
        else:
            pos = pos.left
            while pos.right.getHeight() != -1:
                pos = pos.right
            pos.setRight(elem)
        if i == 0:
            self.setFirst(elem)
        return pos

    """ t.l  or t.right          
         \             \
          U     -->     R
           \          /   \
            R   -->  U     E   
          /   \       \
         a     E -->   a        """

    def rotateLeft(self, u, r):
        u.setRight(r.getLeft())    # set-> u[right]= a
        u.getRight().setParent(u)  # set-> a[parent]= u
        r.setLeft(u)               # set-> r[left] = u
        r.setParent(u.getParent()) # set-> r[parent]= t
        u.setParent(r)             # set-> u[parent]= r
        if u is self.root:
            self.root = r
        else:
            if r.getParent().getRight() == u: # if u is not a root, set his parent to r
                r.getParent().setRight(r)
            else:
                r.getParent().setLeft(r)
        # Fix size & height
        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        r.setSize(r.sUpdate())
        r.setHeight(r.hUpdate())

    def rotateRight(self, u, l):
        u.setLeft(l.getRight())
        u.getLeft().setParent(u)
        l.setRight(u)
        l.setParent(u.getParent())
        u.setParent(l)
        if u is self.root:
            self.root = l
        else:
            if l.getParent().getLeft() == u:
                l.getParent().setLeft(l)
            else:
                l.getParent().setRight(l)

        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        l.setSize(l.sUpdate())
        l.setHeight(l.hUpdate())

    def updateFields(self,u,c):
        u.setSize(u.sUpdate())
        u.setHeight(u.hUpdate())
        c.setSize(c.sUpdate())
        c.setHeight(c.hUpdate())

    """ rebalances the tree upwards starting from node pos
        @type pos: AVLNode
        @param pos: node to start rebalancing upwards
        @returns: number of balancing operations conducted"""
    def fixUp(self, pos, insert=True):
        counter = 0
        while pos is not None:
            #pos.size += (lambda act: 1 if insert else -1)(insert)
            pos.setSize(pos.sUpdate())
            pos.setHeight(pos.hUpdate())
            bf = pos.BFcalc()
            if bf > 1 or bf < -1:
                temp = pos.parent
                if bf == -2 and (lambda bfc: pos.getRight().BFcalc() == -1 if insert else
                        (pos.getRight().BFcalc() == -1 or pos.getRight().BFcalc() == 0))(insert):
                    self.rotateLeft(pos, pos.getRight())
                    counter += 1
                elif bf == -2 and pos.getRight().BFcalc() == 1:
                    self.rotateRight(pos.getRight(), pos.getRight().getLeft())
                    self.rotateLeft(pos, pos.getRight())
                    counter += 2
                elif bf == 2 and (lambda bfc: pos.getLeft().BFcalc() == 1 if insert else
                        (pos.getLeft().BFcalc() == 1 or pos.getLeft().BFcalc() == 0))(insert):
                    self.rotateRight(pos, pos.getLeft())
                    counter += 1
                elif bf == 2 and pos.getLeft().BFcalc() == -1:
                    self.rotateLeft(pos.getLeft(), pos.getLeft().getRight())
                    self.rotateRight(pos, pos.getLeft())
                    counter += 2
                pos = temp

            else:
                pos = pos.parent
        #MIGHT DONT NEED IT
        if self.getSize() == 0:
            self.setRoot(None)
        return counter

    """deletes the i'th item in the list
    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list to be deleted
    @rtype: int
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def delete(self, i, pr=False):
        if self.root is None or i < 0 or i >= self.length():
            return -1
        dNode = self.retrieve_rec(self.root, i + 1,pr)
        self.size -= 1
        # case 1- dNode is a leaf
        if not (dNode.getRight().isRealNode() or dNode.getLeft().isRealNode()):
            pos = self.deleteLeaf(dNode)

        # case 2- dNode has two children
        elif dNode.getRight().isRealNode() and dNode.getLeft().isRealNode():
            sNode = self.findSuccessorD(dNode)  # Find dNode's successor

            if not sNode.getRight().isRealNode() and not sNode.getLeft().isRealNode():
                pos = self.deleteLeaf(sNode)  # case 2.a- sNode is a leaf

            else:  # case 3.b- sNode is a branch
                pos = self.deleteXor(sNode)
            if pos is dNode:  # Edge case- Successor(dNode) == sNode
                pos = sNode
                if self.getLast() is dNode:
                    self.setLast(pos)
            self.exchangeNodes(dNode, sNode)  # set sNode in dNode location

        else:  # XOR(right(isReal(), left(isReal))
            pos = self.deleteXor(dNode)
        return self.fixUp(pos, False)
        # Fixing up to root

    """ deletes a leaf
       @type dNode: AVLNode
       @param dNode: the leaf to be deleted
       @returns: the parent of deleted leaf"""

    def deleteLeaf(self, dNode):
        dnp = dNode.getParent()
        if self.getFirst() is dNode:
            self.setFirst(dnp)
        if self.getLast() is dNode:
            self.setLast(dnp)
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
                dNode.getRight().setParent(dnp)
            else:
                dnp.setLeft(dNode.getLeft())
                dNode.getLeft().setParent(dnp)
        else:
            self.setRoot(None)

        return dnp

    def deleteXor(self, dNode):
        dnp = dNode.getParent()
        if self.getFirst() is dNode:
            self.setFirst(self.getRightMost(dNode.getRight()))
        if self.getLast() is dNode:
            self.setLast(self.getLeftMost(dNode.getLeft()))
        if dNode.getRight().isRealNode():
            dNode.getRight().setParent(dnp)
            if dNode is self.root:
                self.root = dNode.getRight()
                return dnp

            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getRight())
            else:
                dnp.setLeft(dNode.getRight())
        else:
            dNode.getLeft().setParent(dnp)
            if dNode is self.root:
                self.setRoot(dNode.getLeft())
                return dnp
            if dnp.getRight() is dNode:
                dnp.setRight(dNode.getLeft())
            else:
                dnp.setLeft(dNode.getLeft())

        return dnp

    def exchangeNodes(self, dNode, sNode):
        dnp = dNode.getParent()
        sNode.setParent(dNode.getParent())
        sNode.setLeft(dNode.getLeft())
        dNode.getLeft().setParent(sNode)
        if dNode.getRight() is not sNode:
            sNode.setRight(dNode.getRight())
            dNode.getRight().setParent(sNode)
        sNode.setSize(dNode.size)
        if dNode is not self.root:
            if dnp.getRight() is dNode:
                dnp.setRight(sNode)
            else:
                dnp.setLeft(sNode)
        else:
            self.setRoot(sNode)

    def findSuccessorD(self, pos):
        pos = pos.getRight()
        while pos.getLeft().isRealNode():
            pos = pos.getLeft()
        return pos

    """returns the value of the first item in the list
    @rtype: str
    @returns: the value of the first item, None if the list is empty
    """

    def first(self):
        if self.getFirst() is None:
            return None
        return self.getFirst().getValue()

    """returns the value of the last item in the list

    @rtype: str
    @returns: the value of the last item, None if the list is empty
    """

    def last(self):
        if self.getLast() is None:
            return None
        return self.getLast().getValue()

    """returns an array representing list 

    @rtype: list
    @returns: a list of strings representing the data structure
    """

    """real l-to-a func"""

    def listToArray(self):
        ### Travel in tree and then add elements by rank as indexes ###
        res1 = []
        if self.getRoot() is None:
            return res1
        return AVLTreeList.ltoa(self, self.getRoot(), res1)

        return res
    """rec function to return the array
    @type node: AVLNode
    @param: the current node
    @type res: list
    @param res: the list to which we append nodes
    @rtype: list
    @returns: an updated list after adding the nodes
    time Complexity: O(n)"""
    def ltoa(self, node, res):
        if not node.isRealNode():
            return res
        AVLTreeList.ltoa(self, node.getLeft(), res)
        res.append(node.value)
        AVLTreeList.ltoa(self, node.getRight(), res)
        return res

    """returns the size of the list 

    @rtype: int
    @returns: the size of the list
    """

    def length(self):
        return self.getSize()

    """splits the list at the i'th index

    @type i: int
    @pre: 0 <= i < self.length()
    @param i: The intended index in the list according to whom we split
    @rtype: list
    @returns: a list [left, val, right], where left is an AVLTreeList representing the list until index i-1,
    right is an AVLTreeList representing the list from index i+1, and val is the value at the i'th index.
    time complexity: O(log n)
    """

    def split(self, i):
        res = []
        node = self.retNode(self.getRoot(), i)
        leftT = self.createTreefromNode(node.getLeft())
        rightT = self.createTreefromNode(node.getRight())
        val = node.getValue()
        parent = node.getParent()
        while parent != None:
            if parent.getRight() == node:
                node = parent
                parent = node.getParent()
                leftSubTree = self.createTreefromNode(node.getLeft())
                leftT = self.join(leftSubTree, node, leftT)
            else:
                node = parent
                parent = node.getParent()
                rightSubTree = self.createTreefromNode(node.getRight())
                rightT = self.join(rightT, node, rightSubTree)

        # Updating first and last in each tree
        if leftT.getRoot() is not None:
            leftT.setFirst(leftT.getLeftMost(leftT.getRoot()))
            leftT.setLast(leftT.getRightMost(leftT.getRoot()))
            leftT.setSize(leftT.getRoot().getSize())
        if rightT.getRoot() is not None:
            rightT.setFirst(rightT.getLeftMost(rightT.getRoot()))
            rightT.setLast(rightT.getRightMost(rightT.getRoot()))
            rightT.setSize(rightT.getRoot().getSize())
        res.append(leftT)
        res.append(val)
        res.append(rightT)
        return res

    """ creates a new AVL
    @type node: AVLNode
    @param node: the root of the new tree
    @returns: a new tree with node as it's root"""
    def createTreefromNode(self, node : AVLNode):
        Tree = AVLTreeList()
        node.setParent(None)
        Tree.setRoot(node)
        Tree.setSize(node.getSize())
        return Tree

    """ returns the node ar index i
    @type r: AVLNode
    @param r: the current node
    @type i: int
    @param i: the index we want to reach
    @returns: a pointer to the intended node
    time complexity: O(log n)"""
    def retNode(self, r, i):
        smaller = (r.getLeft()).getSize()
        if smaller < i:
            return self.retNode(r.getRight(), i - smaller - 1)
        elif smaller > i:
            return self.retNode(r.getLeft(), i)
        else:
            return r

    """concatenates lst to self
    @type lst: AVLTreeList
    @param lst: a list to be concatenated after self
    @rtype: int
    @returns: the absolute value of the difference between the height of the AVL trees joined
    time complexity: O(log n)
    """

    def concat(self, lst):
        if self.getRoot() is None and lst.getRoot() is None:
            return 0  # both empty trees
        elif self.getRoot() is None:
            height_r = lst.getRoot().getHeight()
            self.setRoot(lst.getRoot())
            self.setSize(lst.getSize())
            self.setFirst(lst.getFirst())
            self.setLast(lst.getLast())
            return height_r +1
        elif lst.getRoot() is None:
            height_l = self.getRoot().getHeight()
            return height_l +1
        height_l = self.getRoot().getHeight()
        height_r = lst.getRoot().getHeight()
        #self.setLast(lst.getLast())
        x = self.getRightMost(self.getRoot())
        #self.setFirst(self.getFirst())
        self.delete(self.length() - 1)
        x.setParent(None)
        joinedTrees = self.join(self, x, lst)
        self.setRoot(joinedTrees.getRoot())
        self.setSize(joinedTrees.getSize())
        self.setFirst(joinedTrees.getLeftMost(joinedTrees.getRoot()))
        self.setLast(joinedTrees.getRightMost(joinedTrees.getRoot()))
        return abs(height_l - height_r)

    """returns the right most node
    @type node: AVLNode
    @param node: the current node
    time complexity: O(log n)"""
    def getRightMost(self, node):
        """if not isinstance(node, AVLNode):
            self.printTree("node not a node")
            return node
        if not isinstance(node.getRight(), AVLNode):
            self.printTree("getRight")
            print(node.getValue())
            return node"""
        while node.getRight().isRealNode():
            node = node.getRight()
        return node

    """returns the left most node
        @type node: AVLNode
        @param node: the current node
        time complexity: O(log n)"""
    def getLeftMost(self, node):
        while node.getLeft().isRealNode():
            node = node.getLeft()
        return node

    """performs a join operation between two trees and x
    @type lst1: AVLTreeList
    @param lst1: the first tree
    @type lst2: AVLTreeList
    @param lst2: the second tree
    @type x: AVLNode
    @param x: the node at which to connect both trees
    @returns: a new AVLTreeList after joining both trees
    time complexity: O(log n)"""
    def join(self, lst1, x: AVLNode, lst2):

        if lst1.empty() and lst2.empty():
            lst2.insert(lst2.getSize(), x.getValue())
            return lst2
        if lst1.empty():
            lst2.insert(0, x.getValue())
            return lst2
        if lst2.empty():
            lst1.insert(lst1.getSize(), x.getValue())
            return lst1

        lst1Height = lst1.getRoot().getHeight()
        lst2Height = lst2.getRoot().getHeight()
        diff = abs(lst1Height - lst2Height)

        if lst1Height == lst2Height or diff == 1:  # no need to rebalance
            x.setLeft(lst1.getRoot())
            x.setRight(lst2.getRoot())
            lst1.getRoot().setParent(x)
            lst2.getRoot().setParent(x)
            self.nodeHandSupdate(x)
            newT = self.createTreefromNode(x)
            return newT

        if lst1Height < lst2Height:
            b = self.reachHeightLeft(lst2, lst1Height)
            x.setLeft(lst1.getRoot())
            lst1.getRoot().setParent(x)
            x.setRight(b)
            c = b.getParent()
            b.setParent(x)
            self.nodeHandSupdate(x)
            x.setParent(c)
            c.setLeft(x)
            self.nodeHandSupdate(c)
            self.fixUp(c, False)
        else:
            b = self.reachHeightRight(lst1, lst2Height)
            x.setLeft(b)
            c = b.getParent()
            b.setParent(x)
            x.setRight(lst2.getRoot())
            lst2.getRoot().setParent(x)
            self.nodeHandSupdate(x)
            x.setParent(c)
            c.setRight(x)
            self.nodeHandSupdate(c)
            self.fixUp(c, False)
        if lst1Height < lst2Height:

            return lst2
        else:
            return lst1

    """ updates the height size of node
    @type node: AVLNode
    @param node: the node we want to update"""
    def nodeHandSupdate(self, node: AVLNode):
        node.setSize(node.getLeft().getSize() + node.getRight().getSize() + 1)
        node.setHeight(max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1)

    """finds a left subtree with height h
    @type tree: AVLTreeList
    @param tree: the tree 
    @type h: int
    @param h: the requested height
    @returns: the root of the requested subtree
    time complexity: O(log n)"""
    def reachHeightLeft(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getLeft()
        return node

    """finds a left subtree with height h
        @type tree: AVLTreeList
        @param tree: the tree 
        @type h: int
        @param h: the requested height
        @returns: the root of the requested subtree
        time complexity: O(log n)"""
    def reachHeightRight(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getRight()
        return node

    """searches for a *value* in the list

       @type val: str
       @param val: a value to be searched
       @rtype: int
       @returns: the first index that contains val, -1 if not found.
       time complexity: O(n)"""

    def search(self, val):
        if self.empty():
            return -1
        node = self.getRoot()
        res = self.search_rec(node, val)
        if res == -1:
            return -1
        else:
            return res
    """actual search func
    @type node: AVLNode
    @param node: the current node we're at
    @type val: str
    @param val: the requested val
    @rtype: int
    @returns the index of the first node containing val
    time complexity: O(n)"""
    def search_rec(self, node, val):
        if not node.isRealNode():
            return -1
        smaller = node.getLeft().getSize()
        if node.getValue() == val:
            return 0 + smaller  # maybe 0??
        left = self.search_rec(node.getLeft(), val)
        if left != -1:
            return left
        right = self.search_rec(node.getRight(), val)
        if right != -1:
            return right + smaller + 1
        return -1

    """returns the root of the tree
    @rtype: AVLNode
    @returns: a pointer to the root
    time complexity: O(1)"""
    def getRoot(self):
        if self.empty():
            return None
        return self.root

    # More functions
    """sets the root of the tree
        @type root: AVLNode
        @param root: the new root of the tree
        @returns: a pointer to the root
        time complexity: O(1)"""
    def setRoot(self, root: AVLNode):
        self.root = root
        #if root != None:
            #self.size = root.getSize()
    """ returns the first node
    @rtype: AVLNode
    @returns: the first item
    time complexity: O(1)"""
    def getFirst(self):
        return self.firstItem

    """sets the first Item
    @type node: AVLNode
    @param node: the node to be set as firstItem
    timecomplexity: O(1)"""
    def setFirst(self, node):
        self.firstItem = node

    """ returns the last node
          @rtype: AVLNode
          @returns: the last item
          time complexity: O(1)"""
    def getLast(self):
        return self.lastItem

    """sets the last Item
       @type node: AVLNode
       @param node: the node to be set as lastItem
       timecomplexity: O(1)"""
    def setLast(self, node):
        self.lastItem = node

    """sets the size of tree
    @type n: int
    @param n: the new size of tree
    time complexity: O(1)"""
    def setSize(self, n):
        self.size = n

    """returns the size of tree
    @rtype: int
    @returns: the size of the tree
    time complexity: O(1)"""
    def getSize(self):
        return self.size

    def select(self, i):
        return self.retrieve_rec(self.root, i + 1)

    def rank(self, val):
        return self.search(val)

    def getTreeHeight(self):
        if self.length() == 0:
            return -1
        return self.getTreeHeightRec(self.getRoot())

    def getTreeHeightRec(self, node):
        if not node.isRealNode():
            return -1
        right = self.getTreeHeightRec(node.getRight())
        left = self.getTreeHeightRec(node.getLeft())
        return max(right, left) + 1

