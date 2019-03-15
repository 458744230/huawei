class Road:
    def __init__(self, input=[]):
        input = list(map(int, input))
        self.id = input[0]
        self.length = input[1]
        self.speed = input[2]
        self.channel = input[3]
        self.from_id = input[4]
        self.to_id = input[5]
        self.isDuplex = input[6]
        self.from_cross = None
        self.to_cross = None

    def getmid(self):
        return (self.from_cross.x + self.to_cross.x) / 2, (self.from_cross.y + self.to_cross.y) / 2
