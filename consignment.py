class Consignment:

    def __init__(self, weight=0, org=None, dst=None):
        self.weight = weight # the consignment weight
        self.m_appear = 0 #
        self.m_load = 0 #
        self.m_unload = 0 #
        self.origin = org # node of destination
        self.destination = dst # node of destination
