"""
this program implements the pseaudocode of the Diagonalize Algorithm given in:
D.P. Jacobs, V. Trevisan, F.C. Tura, Eigenvalue location in cographs, Discrete Appl. Math. 245 (2018) 220–235.

this program also outputs images for the intermediate trees throughout the algorithm

code file by Emily Barranca for MTH  591
University of Rhode Island, Spring 2021
"""
import numpy as np
# import pygraphviz


class node(object):
    """
    create an object with all the info we want to carry around for each node
    """
    def __init__(self,parent, nametag ):
        self.parent = parent
        self.children = []
        self.level = 0
        self.label = None
        self.id= nametag

    def __repr__(self):
        if self.label == None:
            if self.level %2 == 0:
                return "(X) %s" % self.id
            else:
                return "(U) %s" % self.id
        else:
            return str("%s %s" %(self.label ,self.id))

    def add_child(self, kiddo):
        self.children.append(kiddo)

    def get_level(self):
        return self.level
    def set_level(self, lev):
        self.level = lev
    def get_parent(self):
        return self.parent
    def set_parent(self, par):
        self.parent = par
    def get_label(self):
        return self.label
    def set_label(self, lab):
        self.label = lab
    def get_id(self):
        return self.id
    def set_id(self, tag):
        self.id = tag


#####################################################################
def diagonalize(T_G, removed):
    """
    inupt: initial list of values to send to build cotree and a scaler value x
    output: list of diagonal matrix entries corresponding to A(T_G) +xI
    """
    print(T_G)
    # print(len(T_G))
    print(removed)
    #want to kill the whole lowest level so find the lowest level
    depth =0
    for vertex in T_G:
        if vertex.get_level() > depth:
            depth = vertex.get_level()
    print(depth)
    #next pick a pair with same parent
    wholefella = T_G
    while depth >0:
        for vertex in wholefella:
            print("restart wholefella outer loop")
            print(vertex)
            print(vertex.get_level())
            if vertex.get_level()== depth: 
                firstbrother = vertex
                print("\ncandidate for removal: ")
                print(firstbrother)
                T_G.remove(vertex)
                for v2 in T_G:
                    # print("v2")
                    # print(v2)
                    if (v2.get_parent()).get_id() == (firstbrother.get_parent()).get_id():
                        #then we've found a pair
                        alpha = firstbrother.get_label()
                        beta = v2.get_label()
                        print("\nfound a pair")
                        print(firstbrother)
                        print(v2)
                        if depth %2 == 1: #we're at an odd level (parent is X)
                            if (alpha+beta) != 2:
                                v2.set_label((alpha*beta-1)/(alpha+beta -2))
                                removed.append(alpha+beta -2)
                            elif beta ==1:
                                v2.set_label(1)
                                removed.append(0)
                            else:
                                T_G.remove(v2)
                                removed.append(1)
                                removed.append(-(1-beta)**2)
                                print("subcase 1c")
                        else: #even level (parent is a U)
                            if (alpha+beta) != 0:
                                v2.set_label((alpha*beta)/(alpha+beta))
                                removed.append(alpha+beta )
                            elif beta ==0:
                                v2.set_label(0)
                                removed.append(0)
                            else:
                                T_G.remove(v2)
                                removed.append(beta)
                                removed.append(-beta)
                                print("subcase 2c")
                        break
        #maybe iterate thru the leaves still on there
        for nod in T_G:
            #want to remove those and reset their partent' labels
            if nod.get_level() == depth:
                parent = nod.get_parent()
                parent.set_label(nod.get_label())
                T_G.remove(nod)
                # print(nod)
        depth -=1
        wholefella = T_G

    print(T_G)
    return(removed)



def draw_tree(T_G, removed):
    """
    input: cotree and list of removed vertices to add to  the  image
    output: none but updates output images for each set of iters
    """
    pass
    # tree = Digraph()
    # tree.node('0', label = "poop")
    # # print(tree)
    # # tree.format = 'pdf'
    # tree.render()


def build_tree(alist, x):
    """
    input: alist of a_1, a_2, ... a_r values to build a balanced cotree
            and x a scalar to initially label the leaves of the cotree
    output: balanced cotree object T_G(a_1, a_2, ..., a_r-1, 0| 0, ..., 0, a_r)
    """
    #initialize root and a parent for it for cotree
    dummy= node(None, "dummy") #root needs a parent so we don't take it as a pair or throw errors
    root = node(None, "r")
    root.set_label("root")
    root.set_parent(dummy)
    V= [root]
    for i in range(len(alist)):
        ctr=0
        if i == 0: #then parent is root / we're at first level
            for j in range(alist[i]):
                k = node(root, "%d%d" % (i+1,ctr))
                k.set_level(1)
                # k.set_parent(root)
                root.add_child(k)
                V.append(k)
                ctr+=1
        #we're at some other level
        else:
         for vert in V:
            if vert.get_level()== i: #get parent's labeled level
                for j in range(alist[i]): #a_i+1
                    new = node(vert, "%d%d" %(i+1,ctr))
                    new.set_level(i+1)
                    if i == len(alist)-1:
                        new.set_label(x)
                    # new.set_parent(vert)
                    vert.add_child(new)
                    V.append(new)
                    ctr+=1
    return V

#######################################################################
def make_cograph(tree, alist):
    """
    this function takes in a cotree and constructs a cograph
    input: cotree
    output: adjacency matrix for
    """
    #first find number of verts in cograph
    ord = 1
    for a in alist:
        ord = ord*a
    #initialize a matrix of the right size to be all 0s
    adj = np.zeros((ord, ord))
    #bubble up the tree


    return adj

#######################################################################
def find_evals(mat):
    """
    input: adjacency matrix
    output: list of eigenvalues of the matrix
    """
    pass


#######################################################################
if __name__ == '__main__':
    # first determine the list of a_i values
    a_i = [2,2,3]
    x = 1
    #call diagonalize
    T_G = build_tree(a_i, x)
    diag = diagonalize(T_G, [])
    adj = make_cograph(T_G, a_i)
    # print(adj)
    # draw_tree(diag, [])
    # print(diag)
