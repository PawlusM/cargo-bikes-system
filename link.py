class Link:
    """ Link between the net nodes """

    def __init__(self, out_node=None, in_node=None, weight=0):
        # type: (Node, Node, float) -> Link
        self.out_node = out_node
        self.in_node = in_node
        # link length [km]
        self.weight = weight
