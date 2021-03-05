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

def get_tree_depth(tree):
    depth = 0
    for vertex in T_G:
        if vertex.get_level() > depth:
            depth = vertex.get_level()
    return depth

def get_vertices_of_depth(tree, depth):
    """ iterates through the given tree, returning a list of all vertices at the given depth """
    
    vertices = []

    for vertex in tree:
        if vertex.get_level() == depth:
            vertices.append(vertex)

    print(f"vertices at depth {depth}: {vertices}")
    return vertices

def find_brother_pairs(vertices):
    brothers = []
    used_brothers = []
    for vertex1 in vertices:
        for vertex2 in vertices:
            # print(f"vertex1: {vertex1}")
            # print(f"vertex2: {vertex2}")
            
            if vertex1 == vertex2:
                # print(f"these are the same, passing")
                break

            # if we have already used this vertex as a brother, ignore this loop
            if vertex1 in used_brothers:
                print(f"we've used this brother: {vertex1}")
                break

            vertex1_parent = vertex1.get_parent().get_id()
            vertex2_parent = vertex2.get_parent().get_id()
            # print(f"vertex1 parent id: {vertex1_parent}")
            # print(f"vertex2 parent id: {vertex2_parent}")
             
            if vertex1_parent == vertex2_parent:
                used_brothers.append(vertex1)
                print(f"adding {vertex1} to used_brothers list")
                # print(f"Found some brothers! vertex1: {vertex1} vertex2: {vertex2}")
                brothers.append((vertex1, vertex2))

    return brothers

def diagonalize_leah(T_G):
    print(f"Tree: {T_G}")

    depth = get_tree_depth(T_G)
    removed = []

    for current_depth in range(depth, 0, -1):
        # find all vertices at the current level
        vertices = get_vertices_of_depth(T_G, current_depth)

        # find all brother pairs amongst this list of vertices
        brothers = find_brother_pairs(vertices)
        print(f"Brothers: {brothers}")

        # loop through brother list 
        # update removed leaves and labels
        for brother in brothers:
            alpha = brother[0].get_label()
            beta = brother[1].get_label()

            if current_depth %2 == 1: #we're at an odd level (parent is X)
                if (alpha+beta) != 2:
                    brother[1].set_label((alpha*beta-1)/(alpha+beta -2))
                    removed.append(alpha+beta -2)
                    print(f"removing brother 1: {brother[1]}")
                    T_G.remove(brother[0])
                elif beta ==1:
                    brother[1].set_label(1)
                    removed.append(0)
                    T_G.remove(brother[0])
                else:
                    T_G.remove(brother[0])
                    T_G.remove(brother[1])
                    removed.append(1)
                    removed.append(-(1-beta)**2)
                    print("subcase 1c")
            else: #even level (parent is a U)
                if (alpha+beta) != 0:
                    brother[1].set_label((alpha*beta)/(alpha+beta))
                    removed.append(alpha+beta )
                    T_G.remove(brother[0])
                elif beta ==0:
                    brother[1].set_label(0)
                    removed.append(0)
                    T_G.remove(brother[0])
                else:
                    T_G.remove(brother[0])
                    T_G.remove(brother[1])
                    removed.append(beta)
                    removed.append(-beta)
                    print("subcase 2c")

        print(f"Tree after brother loop: {T_G}")
        # relabel parents ~daddiez~
        # remove every leaf at current depth
        vertices_for_relabel = get_vertices_of_depth(T_G, current_depth)

        for vertex in vertices_for_relabel:
            parent = vertex.get_parent()
            parent.set_label(vertex.get_label())
            T_G.remove(vertex)

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
    # diag = diagonalize(T_G, [])
    diag = diagonalize_leah(T_G)
    adj = make_cograph(T_G, a_i)
    # print(adj)
    # draw_tree(diag, [])
    # print(diag)
