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
    """

    def getLeft(self):
        return self.left

    """returns the right child

    @rtype: AVLNode
    @returns: the right child of self, None if there is no right child
    """

    def getRight(self):
        return self.right

    """returns the parent 

    @rtype: AVLNode
    @returns: the parent of self, None if there is no parent
    """

    def getParent(self):
        return self.parent

    """return the value

    @rtype: str
    @returns: the value of self, None if the node is virtual
    """

    def getValue(self):
        return self.value

    """returns the height

    @rtype: int
    @returns: the height of self, -1 if the node is virtual
    """

    def getHeight(self):
        return self.height

    """sets left child

    @type node: AVLNode
    @param node: a node
    """

    def setLeft(self, node):
        self.left = node

    """sets right child

    @type node: AVLNode
    @param node: a node
    """

    def setRight(self, node):
        self.right = node

    """sets parent

    @type node: AVLNode
    @param node: a node
    """

    def setParent(self, node):
        self.parent = node

    """sets value

    @type value: str
    @param value: data
    """

    def setValue(self, value):
        self.value = value

    """sets the balance factor of the node

    @type h: int
    @param h: the height
    """

    def setHeight(self, h):
        self.height = h

    """returns whether self is not a virtual node 

    @rtype: bool
    @returns: False if self is a virtual node, True otherwise.
    """

    def isRealNode(self):
        if self.height == -1:
            return False
        return True

    def getSize(self):
        return self.size

    def setSize(self, s):
        self.size = s

    def BFcalc(self):
        return (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(self)

    def hUpdate(self):
        return (lambda n: max(n.getRight().getHeight(), n.getLeft().getHeight()) + 1)(self)

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

    def retrieve_rec(self, node, i, printNodes=False, counter=1):
        rank = node.getLeft().getSize() + 1
        if rank == i:
            return node
        if i < rank:
            return self.retrieve_rec(node.getLeft(), i, printNodes, counter)
        else:
            return self.retrieve_rec(node.getRight(), i - rank,printNodes,counter)

    """inserts val at position i in the list

    @type i: int
    @pre: 0 <= i <= self.length()
    @param i: The intended index in the list to which we insert val
    @type val: str
    @param val: the value we inserts
    @rtype: list
    @returns: the number of rebalancing operation due to AVL rebalancing
    """

    def append(self, val):
        return self.insert(self.length(), val)

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



    def initNode(self, val):
        elem = AVLNode(val)
        vrNodeR = AVLNode(None, -1, 0)
        vrNodeL = AVLNode(None, -1, 0)
        elem.setRight(vrNodeR)
        elem.setLeft(vrNodeL)
        vrNodeR.setParent(elem)
        vrNodeL.setParent(elem)
        return elem

    def appendNode(self, elem):
        pos = self.root
        while pos.getRight().getHeight() != -1:
            pos = pos.right
        pos.setRight(elem)
        self.setLast(elem)
        return pos

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

    def createTreefromNode(self, node : AVLNode):
        Tree = AVLTreeList()
        node.setParent(None)
        Tree.setRoot(node)
        Tree.setSize(node.getSize())
        return Tree

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

    def getLeftMost(self, node):
        while node.getLeft().isRealNode():
            node = node.getLeft()
        return node

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

    def nodeHandSupdate(self, node: AVLNode):
        node.setSize(node.getLeft().getSize() + node.getRight().getSize() + 1)
        node.setHeight(max(node.getLeft().getHeight(), node.getRight().getHeight()) + 1)

    def reachHeightLeft(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getLeft()
        return node

    def reachHeightRight(self, tree, h):
        node = tree.getRoot()
        while node.getHeight() > h:
            node = node.getRight()
        return node


    def search(self, val):
        if self.empty():
            return -1
        node = self.getRoot()
        res = self.search_rec(node, val)
        if res == -1:
            return -1
        else:
            return res

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

    def getRoot(self):
        if self.empty():
            return None
        return self.root

    # More functions

    def setRoot(self, root: AVLNode):
        self.root = root
        #if root != None:
            #self.size = root.getSize()

    def getFirst(self):
        return self.firstItem

    def setFirst(self, node):
        self.firstItem = node

    def getLast(self):
        return self.lastItem

    def setLast(self, node):
        self.lastItem = node

    def setSize(self, n):
        self.size = n

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

    ######################################## TEST ######################################################################
    ##################################### INSIDE CLASS #################################################################

    """Checks if the AVL tree properties are consistent

    @rtype: boolean 
    @returns: True if the AVL tree properties are consistent
    """

    def check(self, name=""):
        pt = True
        if not self.isAVL():
            print("The tree is not an AVL tree!")
            pt = False
        if not self.isSizeConsistent():
            print("The sizes of the tree nodes are inconsistent!")
            pt = False
        if not self.isHeightConsistent():
            print("The heights of the tree nodes are inconsistent!")
            pt = False

        return pt

    """Checks if the tree is an AVL

    @rtype: boolean 
    @returns: True if the tree is an AVL tree
    """

    def isAVL(self):
        if self.root is None and self.size !=0:
            print("XXX :ERROR: isAVL() --> self.root is None and self.size !=0")
        if self.size == 0:
            return True
        return self.isAVLRec(self.getRoot())

    """Checks if the subtree is an AVL
    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if the subtree is an AVL tree
    """

    def isAVLRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Check abs(balance factor) <= 1
        bf = (lambda n: n.getLeft().getHeight() - n.getRight().getHeight())(x)
        if bf > 1 or bf < -1:
            print("Criminal BF -----> XXXXXXXXX  "+x.getValue()+"  XXXXXXXXXX")
            return False
        # Recursive calls
        return self.isAVLRec(x.getLeft()) and self.isAVLRec(x.getRight())

    """Checks if sizes of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if sizes of the nodes in the tree are consistent
    """

    def isSizeConsistent(self):
        if self.size == 0:
            return True
        return self.isSizeConsistentRec(self.getRoot())

    """Checks if sizes of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if sizes of the nodes in the subtree are consistent
    """

    def isSizeConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            if x.size == 0:
                return True
            else:
                return False
        # Size of x should be x.left.size + x.right.size + 1
        if x.size != (x.getLeft().size + x.getRight().size + 1):
            print("Criminal Size -----> XXX"+str(x.size)+"XXXX  " + x.getValue() + "  XXXX"+str(x.size)+"XXXXXX")
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if heights of the nodes in the tree are consistent

    @rtype: boolean 
    @returns: True if heights of the nodes in the tree are consistent
    """

    def isHeightConsistent(self):
        if self.size == 0:
            return True
        return self.isHeightConsistentRec(self.getRoot())

    """Checks if heights of the nodes in the subtree are consistent

    @type x: AVLNode
    @param x: The root of the subtree
    @rtype: boolean 
    @returns: True if heights of the nodes in the subtree are consistent
    """

    def isHeightConsistentRec(self, x):
        # If x is a virtual node return True
        if not x.isRealNode():
            return True
        # Height of x should be maximum of children heights + 1
        if x.getHeight() != max(x.getLeft().getHeight(), x.getRight().getHeight()) + 1:
            print("Criminal Height -----> XXX ["+str(x.height)+" ]XXXX  " + x.getValue() + "  XXXX[ "+str(x.height)+"] XXXXXX")
            return False
        # Recursive calls
        return self.isSizeConsistentRec(x.getLeft()) and self.isSizeConsistentRec(x.getRight())

    """Checks if the ranks of the nodes in the tree are consistent

    @returns: True if the ranks of the nodes in the tree are consistent
    """

    def isRankConsistent(self):
        root = self.getRoot()
        #for i in range(1, root.size):
            #if i != self.rank(self.retrieve_rec(i + 1)):
                #return False
        nodesList = self.nodes()
        for node in range(len(nodesList)):   # new one
            if self.select(node) is not nodesList[i]:
                return False
        return True

    """Returns a list of the nodes in the tree sorted by index in O(n)

    @rtype: list
    @returns: A list of the nodes in the tree sorted by index
    """

    def nodes(self):
        lst = []
        if self.size ==0:
            return lst
        self.nodesInOrder(self.getRoot(), lst)
        return lst

    """Adds the nodes in the subtree to the list
     following an in-order traversal in O(n)

    @type x: AVLNode
    @type lst: list
    @param x: The root of the subtree
    @param lst: The list
    """

    def nodesInOrder(self, x, lst):
        if not x.isRealNode():
            return
        self.nodesInOrder(x.getLeft(), lst)
        lst.append(x)
        self.nodesInOrder(x.getRight(), lst)

    def oneRandomInsert(self, lst, th="no number", strings=True):
        if not self.check("Before insert: "+str(th)):
            print("Given tree for test { oneRandomInsert } is not correct")
            return False
        treeB = printree(self)
        index = random.randint(0, self.getSize())
        if strings:
            type = random.randint(1, 2)
        else:
            type = 1
        if type == 2:
            lengthStr = random.randint(2, 7)
            val = strGenerator(lengthStr)
        else:
            val = str(random.randint(0, 100))
        self.insert(index, val)
        lst.insert(index, val)
        if not self.check("Before insert: "+str(th)):
            print("before")
            for j in treeB:
                print(j)
            print("Tree after insert val # [" + val + "] # is not correct")
            self.printTree("After")
            return False

        return True

    def oneRandomDelete(self, lst, th="no number", strings=True):
        if not self.check("Before insert: "+str(th)):
            print("Given tree for test { oneRandomInsert } is not correct")
            return False
        treeB = printree(self)
        if self.size == 0:
            return True
        else:
            try:
                index = random.randint(0, self.getSize()-1)
            except:
                print(self.size)

        val = self.retrieve(index)
        self.delete(index)
        del lst[index]
        if not self.check("Before delete: "+str(th)):
            for j in treeB:
                print(j)
            print("Tree after delete val # [" + val + "] # is not correct")
            self.printTree("After")
            return False

        return True

    def randomAct(self, lst, limit=100):
        dec = []
        delCounter = self.getSize()-1
        for i in range(limit):
            dec.append(random.randint(1, 8))
        for b in dec:
            if delCounter > 0 and b % 2 == 1:
                for i in range(b):
                    if delCounter > 0 :
                        one = self.oneRandomDelete(lst, str(i))
                        delCounter -= 1
                    else:
                        one = self.oneRandomInsert(lst, str(i))
                        delCounter += 1
            else:
                one = self.oneRandomInsert(lst, str(i))
                delCounter += 1
            if not one:
                print("mostake in random act")
                return False
        return True



    """ Check if avl tree is handle random insert actions
        :param [ tree, lst, name, limit of insertions]
        """

    def checkInsert(self, lst, name, limit=15):
        passTest = True
        #print("Check insert test (input=#", name, "#):   *(50 inserts)")
        if self.size != len(lst):
            passTest = False
            print("Size of given tree #", name, "# != len(lst) --> ", self.size, "!=", len(lst))
        testAvl = self.check(name)
        if not testAvl:
            print("The criminal is ---->  XXXXXXX  " + val + "  XXXXXXX")
            self.printTree("with criminal " + val + " (size= " + str(self.getSize()) + ")")
        for i in range(limit):
            index = random.randint(0, self.getSize())
            val = str(random.randint(65, 122))
            self.insert(index, val)
            lst.insert(index, val)
            if self.size != len(lst):
                passTest = False
                print("Iter num. ", i + 1, ": Size of the tree #", name + " insert("+str(i)+")", "# != len(lst) --> ", self.size, "!=",
                      len(lst))
            testAvl = self.check(name)
            if not testAvl:
                print("The criminal is ---->  XXXXXXX  " +val + "  XXXXXXX")
                self.printTree("insert("+str(i)+") with criminal "+val+" (size= "+str(self.getSize())+")")
        for i in range(self.size):
            if self.retrieve(i) != lst[i]:
                passTest = False
                print("AVLtree[", i, "] != lst[", i, "] --> # ", self.retrieve(i), " != ", lst[i])
        #if passTest:
            #print("Good! AVL tree #", name, "# passed the test")
        return passTest

    def treeEqList(self, lst):
        if len(lst)!= self.getSize():
            print("Size is not equals in parameters that given")
            return False
        lstN = self.nodes()
        lstV = [lstN[i].value for i in range(self.size)]
        if lstV != lst:
            print("lst given is not equals to AVL tree that given")
            return False
        return True

    """ Given an AVL tree and a list and check if delete of some index not correcrt """
    def checkDelByInOrder(self,lst):
        if not self.treeEqList(lst):
            return False
        for i in range(self.size-1):
            val = self.retrieve(i)
            del lst[i]
            self.delete(i)
            if not self.treeEqList(lst):
                print("val !!! ",val )
                return False
            self.insert(i,val)
            lst.insert(i,val)
        return True

    def checkDeleteRandomly(self, lst, name):
        if not self.treeEqList(lst):
            return False
        passTest = True
        if self.getSize() < 1:
            return True
        delNum = random.randint(1, self.getSize())
        for i in range(delNum):
            index = random.randint(0, self.getSize() - 1)
            avlElem = self.retrieve(index)
            lstElem = lst[index]
            treeBefore = printree(self)
            a = self.delete(index)
            del lst[index]
            if a == -1:
                self.printTree(avlElem)
            self.check(name)
            if not self.validNodes():
                print("delete fuck with "+avlElem)
                for j in treeBefore:
                    print(j)
                print(lstElem)
                print(lst)
                return False
            # CHECK IF LST==AVL
            for j in range(self.getSize()):
                rIndex = random.randint(0, self.getSize() - 1)
                if self.retrieve(rIndex) != lst[rIndex]:
                    if self.retrieve(rIndex) == False:
                        self.printTree("ret fuck ["+str(rIndex)+"]")
                        self.lstDetails()

                    passTest = False
                    print("AVLtree[", rIndex, "] != lst[", rIndex, "] --> # ", self.retrieve(rIndex), " != ",
                          lst[rIndex])
                    print("Criminal deletion --> AVL[", index, "]:", avlElem, "|| lst[", index, "]:", lstElem)
        return passTest
        #if passTest:
            #print("###########################\nGood! AVL tree #", name, "# passed the test\n###################################")

    def printTree(self, name=""):
        print("AVL tree: ", name)
        tLst = printree(self)
        for n in tLst:
            print(n)

    def validNodes(self):
        nodesLst = self.nodes()
        for i in nodesLst:
            if not isinstance(i, AVLNode):
                print("there is none in lst")
                return False
        return True

    def lstDetails(self):
        nodesLst = self.nodes()
        lstV = [nodesLst[j].value for j in range(len(nodesLst))]
        lstS = [nodesLst[j].getSize() for j in range(len(nodesLst))]
        lstH = [nodesLst[j].getHeight() for j in range(len(nodesLst))]
        lstB = [nodesLst[j].BFcalc() for j in range(len(nodesLst))]
        laN = lambda x: "None!" if x is None else x.getValue()
        # laN2 =
        lstD = [[laN(nodesLst[j].getLeft()), laN(nodesLst[j].getParent()), laN(nodesLst[j].getRight())] for j in
                range(len(nodesLst))]
        print(lstV)
        print(lstS)
        print(lstH)
        print(lstB)
        print(lstD)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

""" Lists generator
:rType: (AVL tree , Array) 
:return: AVL tree list , Array list
"""
def listsGenerator(limit):
    t = AVLTreeList()
    lst = []
    chooseLen = random.randint(0, limit)
    for i in range(chooseLen):
        val = valGenerator()
        index = random.randint(0, i)
        t.insert(index, val)
        lst.insert(index, val)
        t.check("random generator")

    return t, lst

def valGenerator():
    chooseType = random.randint(1, 3)  # 3-> string , 2 -> int, 1 -> char
    if chooseType == 3:
        lengthStr = random.randint(2, 7)
        val = strGenerator(lengthStr)
    elif chooseType == 2:
        val = str(random.randint(0, 100))
    else:
        val = chr(random.randint(97, 122))
    return val

def strGenerator(len):
    res = [chr(random.randint(65, 90)) for i in range(len)]
    return "".join(res)


def arrayPrinter(t):
    lt = t.nodes()
    lb = []
    lv = []
    for k in range(len(lt)):
        e = []
        d = []
        if not isinstance(lt[k], AVLNode):
            print("None node in lt[", k, "] -> should be a vr!")
            lv.append("None")
            d.append("None -->")
        else:
            if lt[k].value is None:
                lv.append("VR")
                d.append("VR -->")
            else:
                lv.append(lt[k].value)
                d.append(lt[k].value + " -->")

        if not isinstance(lt[k].left, AVLNode):
            print("None node in lt[", k, "].Left -> should be a vr!")
            e.append("N")
        else:
            if lt[k].left is None:
                e.append("VR")
            else:
                e.append(lt[k].left.value)

        if not isinstance(lt[k].parent, AVLNode) and lt[k] is not t.root:
            print("None node in lt[", k, "].parent -> not root, so it is a mistake")
        else:
            if lt[k].parent is None:
                e.append("None of root")
            else:
                e.append(lt[k].parent.value)

        if not isinstance(lt[k].right, AVLNode):
            print("None node in lt[", k, "].Right -> should be a vr!")
        else:
            if lt[k].right is None:
                e.append("VR")
            else:
                e.append(lt[k].right.value)
        d.append(e)
        lb.append(d)
    if len(lt) != len(lb):
        print("sizes not good")
    print("\nList of values in order: ", lv)
    print("List of branches in order: ", lb, "\n")


def main():
    t1, t2, t3 = AVLTreeList(), AVLTreeList(), AVLTreeList()
    l1 = [str(i) for i in range(10)]  # [0, 1, 2, 3, ... , 9]
    l2 = [str(i) for i in range(0, 20, 2)]  # [0, 2, 4, 6, ... , 18]
    l3 = [chr(i) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']
    i1 = [t1.insert(i, str(i)) for i in range(10)]  # [0, 1, 2, 3, ... , 9]
    i2 = [t2.insert(i / 2, str(i)) for i in range(0, 20, 2)]  # [0, 2, 4, 6, ... , 18]
    i3 = [t3.insert(i - 65, chr(i)) for i in range(65, 91)]  # ['a', 'b', 'c', ... , 'z']
    #t3.printTree()
    t4 = AVLTreeList()
    t4.append("e")
    t4.append("g")
    t4.insert(0,"c"), t4.insert(2,"f")
    t4.append("i"), t4.insert(1, "d")
    t4.insert(0, "a"), t4.insert(6,"h")
    t4.insert(1, "b")
    t4.printTree()
    print(t4.getTreeHeight())
    arr = t4.listToArray()
    print(arr)
    lst4 = ["a", "b", "c", "d", "e", "f", "g", "h","i"]


#################################################################################################
#################################################################################################

                                  ### PRINTER FUNCTION ###
def printree(t, bykey=False):
    """Print a textual representation of t
    bykey=True: show keys instead of values"""
    return trepr(t, t.getRoot(), bykey)


def trepr(t, node, bykey=False):
    """Return a list of textual representations of the levels in t
    bykey=True: show keys instead of values"""
    if not isinstance(node, AVLNode):
        return ["None"]

    if not node.isRealNode():  # You might want to change this, depending on your implementation
        return ["#"]  # Hashtag marks a virtual node

    thistr = str(node.getValue())

    return conc(trepr(t, node.getLeft(), bykey), thistr, trepr(t, node.getRight(), bykey))


def conc(left, root, right):
    """Return a concatenation of textual representations of
    a root node, its left node, and its right node
    root is a string, and left and right are lists of strings"""

    lwid = len(left[-1])
    rwid = len(right[-1])
    rootwid = len(root)

    result = [(lwid + 1) * " " + root + (rwid + 1) * " "]

    ls = leftspace(left[0])
    rs = rightspace(right[0])
    result.append(ls * " " + (lwid - ls) * "_" + "/" + rootwid * " " + "\\" + rs * "_" + (rwid - rs) * " ")

    for i in range(max(len(left), len(right))):
        row = ""
        if i < len(left):
            row += left[i]
        else:
            row += lwid * " "

        row += (rootwid + 2) * " "

        if i < len(right):
            row += right[i]
        else:
            row += rwid * " "

        result.append(row)

    return result


def leftspace(row):
    """helper for conc"""
    # row is the first row of a left node
    # returns the index of where the second whitespace starts
    i = len(row) - 1
    while row[i] == " ":
        i -= 1
    return i + 1


def rightspace(row):
    """helper for conc"""
    # row is the first row of a right node
    # returns the index of where the first whitespace ends
    i = 0
    while row[i] == " ":
        i += 1
    return i


if __name__ == "__main__":
    main()


