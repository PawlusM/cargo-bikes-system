import stochastic


class Node:
    """ Node of the transport net """

    def __init__(self, code=0, name=""):
        self.code = code
        if name is "":
            self.name = "Node" + str(code)
        else:
            self.name = name
        # graph features
        self.out_links = []
        self.in_links = []
