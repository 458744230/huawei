class Road:
    def __init__(self, input=[]):
        self.id = input[0]
        self.length = input[1]
        self.speed = input[2]
        self.channel = input[3]
        self.fro = input[4]
        self.to = input[5]
        self.isDuplex = input[6]