class Cross:
    def __init__(self, input=[]):
        input = list(map(int, input))
        self.id = input[0]
        self.roadId = input[1:]
        self.road = [None] * 4
        self.x = 0
        self.y = 0
        self.flag = 0

    def next_cross(self, pos):
        if pos < 0 | pos > 3:
            return None
        if self == self.road[pos].from_cross:
            return self.road[pos].to_cross
        else:
            return self.road[pos].from_cross

    def setpos(self, x, y):
        self.x = x
        self.y = y
        self.flag = 1
