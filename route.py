class Route:

    def __init__(self, net=None):
        self.nodes = []
        self.net = net # net on which the route is defined

    @property
    def size(self):
        return len(self.nodes)

    @property
    def distance(self):
        if self.size == 0 or self.net is None:
            return None
        else:
            d = 0
            sdm = self.net.floyd_warshall
            for i in range(self.size - 1):
                 d += sdm[self.nodes[i].code][self.nodes[i + 1].code]
            return d

    def merge(self, other_route):
        pass
