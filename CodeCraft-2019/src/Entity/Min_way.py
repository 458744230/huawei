# -----coding:utf-8------
'''
@project:huawei
@author:yixu
@file:minway.py
@ide:PyCharm
@create_time:2019/3/16 9:56
使用弗洛伊德算法，先写出邻接矩阵，距离为权值，求出所有的cross到cross的最短路径，并返回最短路径的二维矩阵。
'''

INF = 10000000  # 设置最大值；


class Min_way:
    def __init__(self, road_list, cross_size=128, channel_weight = 0):
        cross_size += 1
        min_num = 10000000  # 最小的cross点
        max_num = -1  # 最大的cross点
        cross_len = [([0] * cross_size) for p in range(cross_size)]  # 初始化最短路径数组
        for i in range(cross_size):
            for j in range(cross_size):
                cross_len[i][j] = INF

        path = [([0] * cross_size) for p in range(cross_size)]  # 初始化最短路径中间经过的节点
        for i in range(cross_size):
            for j in range(cross_size):
                path[i][j] = INF
        for road in road_list:
            cross_len[road.from_id][road.to_id] = road.length / road.speed / (road.channel ** channel_weight)
            # 得到路径权值，注意这里除了速度
            min_num = min(road.from_id, min_num, road.to_id)
            max_num = max(road.from_id, max_num, road.to_id)
            if road.is_duplex == 1:  # 双向道赋值相反的道路
                cross_len[road.to_id][road.from_id] = road.length / road.speed / (road.channel ** channel_weight)


        for k in range(min_num, max_num + 1):
            for i in range(min_num, max_num + 1):
                for j in range(min_num, max_num + 1):
                    if (cross_len[i][k] != INF and cross_len[k][j] != INF and (cross_len[i][k] + cross_len[k][j]) <
                            cross_len[i][j]):
                        cross_len[i][j] = (cross_len[i][k] + cross_len[k][j])  # 弗洛伊德算法更新
                        path[i][j] = k

        cross_to_road = [[None] * cross_size for _ in range(cross_size)]
        for road in road_list:
            cross_to_road[road.from_id - 1][road.to_id - 1] = road.id
            if road.is_duplex == 1:
                cross_to_road[road.to_id - 1][road.from_id - 1] = road.id

        self.path = path
        self.min_way = cross_len
        self.cross_to_road = cross_to_road

    def getminway(self):
        return self.min_way  # 返回

    def getpath(self, visit_path, path, start_node, end_node):
        temp_point = path[start_node][end_node]
        if (temp_point == INF):
            return
        else:
            self.getpath(visit_path, path, start_node, temp_point)
            visit_path.append(temp_point)
            self.getpath(visit_path, path, temp_point, end_node)

    def returnvisitpath(self, start_node, end_node):
        visit_path = []
        visit_path.append(start_node)
        self.getpath(visit_path, self.path, start_node, end_node)
        visit_path.append(end_node)
        return visit_path

    def mini_road(self, start_node, end_node):
        visit_path = self.returnvisitpath(start_node, end_node)
        mini_road_path = []
        for i in range(1, visit_path.__len__()):
            temp_road_id = self.cross_to_road[visit_path[i - 1] - 1][visit_path[i] - 1]
            mini_road_path.append(temp_road_id)
        return mini_road_path

