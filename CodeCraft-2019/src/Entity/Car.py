class Car:
    def __init__(self, input=[]):
        input = list(map(int, input))
        self.id = input[0]
        self.fro = input[1]
        self.to = input[2]
        self.speed = input[3]
        self.planTime = input[4]
