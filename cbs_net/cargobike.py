class CargoBike:

    def __init__(self, capacity=100000):
        self.capacity = capacity  # [g]
        self.length = 800     # [mm]
        self.width = 500
        self.height = 400
        self.velocity = 20  # km/h
        # routes to implement
        self.routes = []

    @property
    def dim(self):
        return self.length, self.width, self.height
