class Map:
    def __init__(self, road_list, cross_list):
        tempDict = []
        for road in road_list:
            tempDict[road.id] = road
        for cross in cross_list:
            for i in range(4):
                cross.road[i] = tempDict[cross.roadId[i]]
        tempDict = []
        for cross in cross_list:
            tempDict[cross.id] = cross
        for road in road_list:
            road.from_cross = tempDict[road.from_id]
            road.to_cross = tempDict[road.to_id]

        zero_cross = None
        # 暂时将-1，*，*，-1的cross当作左上顶点
        for cross in cross_list:
            if cross.roadId[0] == -1 & cross.roadId[3] == -1:
                zero_cross = cross

        self.zero_cross = zero_cross
        self.road_list = road_list
        self.cross_list = cross_list
