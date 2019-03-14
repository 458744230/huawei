import matplotlib.pyplot as plt
import queue


class Map:
    def __init__(self, road_list, cross_list):
        temp_dict = {}
        for road in road_list:
            temp_dict[road.id] = road
        for cross in cross_list:
            for i in range(4):
                cross.road[i] = temp_dict.get(cross.roadId[i], None)
        temp_dict = {}
        for cross in cross_list:
            temp_dict[cross.id] = cross
        for road in road_list:
            road.from_cross = temp_dict[road.from_id]
            road.to_cross = temp_dict[road.to_id]

        zero_cross = None
        # 暂时将-1，*，*，-1的cross当作左上顶点
        for cross in cross_list:
            if cross.roadId[0] == -1 & cross.roadId[3] == -1:
                zero_cross = cross

        self.zero_cross = zero_cross
        self.road_list = road_list
        self.cross_list = cross_list

    def plot(self):

        self.zero_cross.setpos(10, 10)
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
            if c0.road[0] is not None and c0.next_cross(0).flag == 0:
                que.put(c0.next_cross(0))
                c0.next_cross(0).setpos(x, y - c0.road[0].length)
                X.append(x)
                Y.append(y - c0.road[0].length)
            if c0.road[1] is not None and c0.next_cross(1).flag == 0:
                que.put(c0.next_cross(1))
                c0.next_cross(1).setpos(x + c0.road[1].length, y)
                X.append(x + c0.road[1].length)
                Y.append(y)
            if c0.road[2] is not None and c0.next_cross(2).flag == 0:
                que.put(c0.next_cross(2))
                c0.next_cross(2).setpos(x, y + c0.road[2].length)
                X.append(x)
                Y.append(y + c0.road[2].length)
            if c0.road[3] is not None and c0.next_cross(3).flag == 0:
                que.put(c0.next_cross(3))
                c0.next_cross(3).setpos(x - c0.road[3].length, y)
                X.append(x - c0.road[3].length)
                Y.append(y)
        plt.scatter(X, Y)
        plt.show()
