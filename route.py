class Route:

    def __init__(self, net=None, csts=[]):
        self.consignments = csts
        self.net = net # net on which the route is defined

    def __str__(self):
        ans = "Route["
        if self.sender is None:
            ans += "None]{"
        else:
            ans += str(self.sender.code) + "]{"
        if self.size > 0:
            for n in self.nodes[:-1]:
                ans += str(n.code) + "--"
            ans += str(self.nodes[-1].code)
        ans += "}(" + str(self.size) + "): " + str(self.weight)
        return ans

    @property
    def sender(self):
        if self.size == 0 or self.net is None:
            return None
        else:
            # the same sender for all consignments!!!
            return self.consignments[0].origin

    @property
    def nodes(self):
        return [self.sender] + [c.destination for c in self.consignments] + [self.sender]

    @property
    def size(self):
        return len(self.consignments)

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

    @property
    def weight(self):
        return sum([c.weight for c in self.consignments])

    def merge(self, other):
        if (other is not None) and (self.net is other.net):
            self.consignments += other.consignments
