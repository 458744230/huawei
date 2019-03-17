# -----coding:utf-8------
import matplotlib.pyplot as plt
import queue

from matplotlib.lines import Line2D


class Map:
    def __init__(self, road_list, cross_list, car_list):
        temp_dict = {}
        for road in road_list:
            temp_dict[road.id] = road
        for cross in cross_list:
            for i in range(4):
                cross.road[i] = temp_dict.get(cross.roadId[i], None)
        temp_dict = {}
        for cross in cross_list:
            temp_dict[cross.id] = cross
        # 创建是否有路的邻接矩阵
        cross_to_road = [[None]*cross_list.__len__() for i in range(cross_list.__len__())]
        for road in road_list:
            cross_to_road[road.from_id-1][road.to_id-1] = road.id
            if road.is_duplex == 1:
                cross_to_road[road.to_id-1][road.from_id-1] = road.id
            road.from_cross = temp_dict[road.from_id]
            road.to_cross = temp_dict[road.to_id]
        for car in car_list:
            car.from_cross = temp_dict[car.fro]
            car.to_cross = temp_dict[car.to]

        zero_cross = None
        # 暂时将-1，*，*，-1的cross当作左上顶点
        for cross in cross_list:
            if cross.roadId[0] == -1 & cross.roadId[3] == -1:
                zero_cross = cross

        self.zero_cross = zero_cross
        self.road_list = road_list
        self.cross_list = cross_list
        self.car_list = car_list
        self.plot_car = False
        self.cross_to_road = cross_to_road

    def plot(self):

        _, ax = plt.subplots()
        self.zero_cross.set_pos(10, 10)
        X = [10]
        Y = [10]
        que = queue.Queue()
        que.put(self.zero_cross)
        while not que.empty():
            c0 = que.get()
            if c0 is None:
                continue
            x = c0.x
            y = c0.y
            plt.annotate(c0.id, xy=(x, y))
            if c0.road[0] is not None and c0.next_cross(0).flag == 0:
                que.put(c0.next_cross(0))
                c0.next_cross(0).set_pos(x, y - c0.road[0].length)
                X.append(x)
                Y.append(y - c0.road[0].length)
            if c0.road[1] is not None and c0.next_cross(1).flag == 0:
                que.put(c0.next_cross(1))
                c0.next_cross(1).set_pos(x + c0.road[1].length, y)
                X.append(x + c0.road[1].length)
                Y.append(y)
            if c0.road[2] is not None and c0.next_cross(2).flag == 0:
                que.put(c0.next_cross(2))
                c0.next_cross(2).set_pos(x, y + c0.road[2].length)
                X.append(x)
                Y.append(y + c0.road[2].length)
            if c0.road[3] is not None and c0.next_cross(3).flag == 0:
                que.put(c0.next_cross(3))
                c0.next_cross(3).set_pos(x - c0.road[3].length, y)
                X.append(x - c0.road[3].length)
                Y.append(y)
        for road in self.road_list:
            points = [road.from_cross.get_pos(), road.to_cross.get_pos()]
            (x, y) = zip(*points)
            if road.is_duplex == 1:
                ax.add_line(Line2D(x, y, linewidth=road.channel,
                                   color='blue'))
                plt.annotate('%d/%d' % (road.id, road.channel), xy=road.get_mid())
            else:
                ax.add_line(Line2D(x, y, linewidth=road.channel,
                                   color='red', linestyle='-.'))
                plt.annotate('%d/%d' % (road.id, road.channel), xy=road.get_mid())
        if self.plot_car:
            for car in self.car_list:
                points = [car.from_cross.get_pos(), car.to_cross.get_pos()]
                (x, y) = zip(*points)
                ax.add_line(Line2D(x, y, color='yellow', linestyle='-.'))
                plt.annotate('%d/%d' % (car.id, car.planTime), xy=car.get_mid())

        plt.plot()
        plt.scatter(X, Y)
        plt.show()
