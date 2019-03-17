# -----coding:utf-8------
class Road:
    def __init__(self, input_data=[]):
        input_data = list(map(int, input_data))
        self.id = input_data[0]
        self.length = input_data[1]
        self.speed = input_data[2]
        self.channel = input_data[3]
        self.from_id = input_data[4]
        self.to_id = input_data[5]
        self.is_duplex = input_data[6]
        self.from_cross = None
        self.to_cross = None
        # 道路上的车，未调度和已调度的车才能暂时共存，
        # 维度依次为方向、车道、位置、调度与未调度车辆
        self.car_in_road = [[[[None] * 2 for i in range(self.length)]
                             for j in range(self.channel)]
                            for k in range(self.is_duplex + 1)]
        # 保存车辆停留信息 key:时间片 value:车数量  暂时忽略其他车导致的速度减少
        self.history = {}
        # 拥堵程度，history对应的同一时间片内最大车数
        self.congestion = 0

    def get_mid(self):
        return (self.from_cross.x + self.to_cross.x) / 2, (self.from_cross.y + self.to_cross.y) / 2

    # 往路上添加车，如果没有已调度的车就能停,车确实移动之后把原来的位置腾出来
    # 输入车对象本身，当前位置（不在此road上时为-1），能移动的最远距离，系统当前时间
    def add_car(self, car, to, direction, now_time):
        chs = self.car_in_road[direction]
        for i in range(self.channel):
            for j in range(to):
                if chs[i][j][0] is None or chs[i][j][0].now_time == now_time:  # 可以开
                    if chs[i][j][0] is None:  # 无障碍
                        chs[i][j][0] = car
                    else:  # 障碍车为调度，假设一定会开走  TODO
                        chs[i][j][1] = car
                    # 车调度完成，从旧的位置删除
                    car.now_time = now_time + 1
                    old_road, old_dir, old_ch, old_pos = car.get_pos()
                    if old_road is not None:
                        old_p = old_road.car_in_road[direction][old_ch][old_pos]
                        old_p[0] = None
                        if old_p[1] is not None:
                            old_p[0] = old_p[1]
                    car.set_pos(self, direction, i, j)
                    return 1
        # 无法调度，异常
        return 0

    # 处理所有不过cross的车，从靠近终点的车开始执行,即其后的车都是已调度的
    def drive_car(self, car, now_time):
        _, old_dir, old_ch, old_pos = car.get_pos()
        max_v = min(car.speed, self.speed)
        if self.car_in_road[old_dir][old_ch][old_pos + 1][0] is not None:
            # 无法调度,停车
            car.now_time = now_time + 1
            return
        next_pos = min(self.length - 1, max_v + old_pos) # 若没有障碍车，则停到能停最远的位置
        for i in range(old_pos + 2, min(self.length, max_v + old_pos + 1)):
            if self.car_in_road[old_dir][old_ch][i][0] is not None:
                # 发现障碍车
                next_pos = i - 1
        # 停车
        car.set_pos(self, old_dir, old_ch, next_pos)
        # 腾出原来的位置
        if self.car_in_road[old_dir][old_ch][old_pos][1] is not None:
            self.car_in_road[old_dir][old_ch][old_pos][0] = self.car_in_road[old_dir][old_ch][old_pos][1]
            self.car_in_road[old_dir][old_ch][old_pos][1] = None
        else:
            self.car_in_road[old_dir][old_ch][old_pos][0] = None
        # 调度完成
        car.now_time = now_time + 1
        return

    def calculate_congestion(self):
        max_value = 0
        for key, value in self.history.items():
            max_value = max_value if max_value > value else value
        self.congestion = max_value
        return max_value
