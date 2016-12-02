class BiCluster:
    def __init__(self, vec, left=None, right=None, distance=0.0, id=None):
        """
        Each cluster in hierarchical clustering algorithm is either a point in the tree with 2 branches (left and right) or an
        endpoint associated with an actual row from the dataset
        :param vec:
        :param left:
        :param right:
        :param distance:
        :param id:
        """
        self.vec = vec
        self.left = left
        self.right = right
        self.distance = distance
        self.id = id
