class Road:
    def __init__(self, input=[]):
        self.id = input[0]
        self.length = input[1]
        self.speed = input[2]
        self.channel = input[3]
        self.from_id = input[4]
        self.to_id = input[5]
        self.isDuplex = input[6]
        self.from_cross = None
        self.to_cross = None
