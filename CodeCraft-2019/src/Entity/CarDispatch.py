import random


class Dispatch:
    def __init__(self, car_list, cross_num):
        D = [[[] for _ in range(cross_num)] for _ in range(cross_num)]
        max_value = 0
        min_value = float('inf')
        for car in car_list:
            D[car.fro - 1][car.to - 1].append(car)
            if car.speed < min_value:
                min_value = car.speed
            if car.speed > max_value:
                max_value = car.speed
        valid_pair = [(i, j) for i in range(cross_num) for j in range(cross_num) if D[i][j].__len__() > 0]
        table = []
        for pair in valid_pair:
            D[pair[0]][pair[1]].sort(key=lambda x: x.speed, reverse=True)
            table += [pair] * D[pair[0]][pair[1]].__len__()
        self.table = table
        self.D = D
        self.valid_pair = valid_pair
        self.max_speed = max_value
        self.min_speed = min_value

    def pop(self):
        choose = random.choice(self.table)
        car = self.D[choose[0]][choose[1]][0]
        self.table.remove(choose)
        self.D[choose[0]][choose[1]].remove(car)
        return car
