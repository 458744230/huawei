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
    def __init__(self, road_list):
        min_num = 10000000  # 最小的cross点
        max_num = -1  # 最大的cross点
        cross_len = [([0] * 10000) for p in range(10000)]  # 初始化最短路径数组
        for i in range(10000):
            for j in range(10000):
                cross_len[i][j] = INF

        path = [([0] * 10000) for p in range(10000)]  # 初始化最短路径中间经过的节点
        for i in range(10000):
            for j in range(10000):
                path[i][j] = INF

        for road in road_list:
            cross_len[road.from_id][road.to_id] = road.length / road.speed  # 得到路径权值，注意这里除了速度
            min_num = min(road.from_id, min_num, road.to_id)
            max_num = max(road.from_id, max_num, road.to_id)
            if road.is_duplex == 1:
                cross_len[road.to_id][road.from_id] = road.length / road.speed  # 双向道赋值相反的道路

        for k in range(min_num, max_num + 1):
            for i in range(min_num, max_num + 1):
                for j in range(min_num, max_num + 1):
                    if (cross_len[i][k] != INF and cross_len[k][j] != INF and (cross_len[i][k] + cross_len[k][j]) <
                            cross_len[i][j]):
                        cross_len[i][j] = (cross_len[i][k] + cross_len[k][j])  # 弗洛伊德算法更新
                        path[i][j] = k
        self.path = path
        self.min_way = cross_len

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
