class Consignment:

    def __init__(self, weight=0, org=None, dst=None):
        self.weight = weight # the consignment weight
        self.origin = org # node of origin
        self.destination = dst # node of destination
        # events moments
        self.m_appear = 0 #
        self.m_load = 0 #
        self.m_unload = 0 #
