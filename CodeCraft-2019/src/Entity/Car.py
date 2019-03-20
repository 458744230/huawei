# -----coding:utf-8------
class Car:
    def __init__(self, input_data=[]):#car的数据结构，from_cross为指针，拼接
        input_data = list(map(int, input_data))
        self.id = input_data[0]
        self.fro = input_data[1]
        self.to = input_data[2]
        self.speed = input_data[3]
        self.plan_time = input_data[4]
        self.from_cross = None
        self.to_cross = None
        self.now_time = self.plan_time
        self.road = None
        self.pos = 0
        self.ch = 0
        self.direction = 0
        self.sort_to_go = 0

    def get_mid(self):#画车道图用的
        return (self.from_cross.x + self.to_cross.x) / 2, (self.from_cross.y + self.to_cross.y) / 2

    def set_pos(self, road, direction, ch, pos):
        self.road = road
        self.pos = pos
        self.ch = ch
        self.direction = direction

    def get_pos(self):
        return self.road, self.direction, self.ch, self.pos
