class Car:
    def __init__(self, input=[]):
        input = list(map(int, input))
        self.id = input[0]
        self.fro = input[1]
        self.to = input[2]
        self.speed = input[3]
        self.planTime = input[4]
        self.from_cross = None
        self.to_cross = None

    def getmid(self):
        return (self.from_cross.x + self.to_cross.x) / 2, (self.from_cross.y + self.to_cross.y) / 2

