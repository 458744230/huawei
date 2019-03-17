class Cross:
    def __init__(self, input_data=[]):
        input_data = list(map(int, input_data))
        self.id = input_data[0]
        self.roadId = input_data[1:]
        self.road = [None] * 4
        self.x = 0
        self.y = 0
        self.flag = 0
        self.magical_garage = []  # 车库里的车应按计划出行时间-id 升序排序

    def next_cross(self, pos):
        if pos < 0 | pos > 3:
            return None
        if self == self.road[pos].from_cross:
            return self.road[pos].to_cross
        else:
            return self.road[pos].from_cross

    def set_pos(self, x, y):
        self.x = x
        self.y = y
        self.flag = 1

    def get_pos(self):
        return self.x, self.y

    def add_car_from_garage(self, now_time):
        for car in self.magical_garage:
            if car.plan_time > now_time:
                break
            direction = 0 if self == self.road[0].from_cross else 1
            road = self.road[0][direction]  # TODO  找到路线和方向

            for i in self.road[0].channel:
                if road[i][0][0] is not None:
                    continue
                next_pos = min(car.speed, self.road[0].speed)
                for j in range(2, min(car.speed, self.road[0].speed) + 1):
                    if road[i][j][0] is not None:
                        next_pos = j - 1
                road[i][next_pos][0] = car
                car.set_pos(self.road[0], direction, i, next_pos)
                self.magical_garage.remove(car)
                continue
            # 会到这里就说没有位置塞新车了
            break
