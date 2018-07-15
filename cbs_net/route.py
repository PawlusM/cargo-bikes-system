import numpy as np


class Route:

    def __init__(self, net=None, csts=[]):
        self.consignments = csts
        self.net = net # net on which the route is defined
        self.sdm = np.array([[]]) # shortest distances matrix
        if net is not None:
            self.sdm = self.net.floyd_warshall


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
        ans += "}" + "({}): {} km, {} tons, {} tkm".format(self.size,
               round(self.distance, 3), round(self.weight, 3), round(self.transport_work, 3))
        return ans

    @property
    def size(self):
        return len(self.consignments)

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
    def distance(self):
        if self.size == 0 or self.net is None:
            return None
        else:
            d = 0
            for i in range(1, len(self.nodes)):
                 d += self.sdm[self.nodes[i - 1].code][self.nodes[i].code]
            return d

    @property
    def transport_work(self):
        if self.size == 0 or self.net is None:
            return None
        else:
            w = 0
            vol = self.weight
            for i in range(1, len(self.nodes) - 1):
                 w += self.sdm[self.nodes[i - 1].code][self.nodes[i].code] * vol
                 vol -= self.consignments[i - 1].weight
            return w

    @property
    def weight(self):
        return sum([c.weight for c in self.consignments])

    @property
    def weights(self):
        return [c.weight for c in self.consignments]

    def merge(self, other):
        if (other is not None) and (self.net is other.net):
            self.consignments += other.consignments
