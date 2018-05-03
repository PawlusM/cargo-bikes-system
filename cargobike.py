class CargoBike:

    def __init__(self, capacity=100):
        self.capacity = capacity
        self.length = 0
        self.width = 0
        self.height = 0
        self.velocity = 20 # km/h
        # routes to implement
        self.routes = []

    @property
    def dim(self):
        return (self.length, self.width, self.height)
