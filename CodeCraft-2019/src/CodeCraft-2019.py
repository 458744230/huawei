# -----coding:utf-8------
import logging
import numpy as np
import sys
import Entity
import math

np.set_printoptions(threshold=np.inf)

logging.basicConfig(level=logging.DEBUG,
                    filename='../../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')


def main():
#强哥nb
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    car_list, cross_list, road_list = Entity.read(car_path, cross_path, road_path)
    # write_route(car_list,cross_list.__len__())
    # car_list.sort(key=lambda x: x.speed, reverse=True)
    mini_way = Entity.Min_way(road_list)
    my_map = Entity.Map(road_list, cross_list, car_list)
    my_map.partition()
    # my_map.plot()
    # for i in range(car_list.__len__()):
    #     car_list[i].sort_to_go = i + 1
    # for j in range(2):
    #     for i in range(my_map.car_list_v2[j].__len__()):
    #         my_map.car_list_v2[j][i].sort_to_go = i + 1
    # write_result(answer_path, car_list, my_map, mini_way)
    write_result_v2(answer_path, my_map, mini_way)
    # calculate_all_congestion(car_list, road_list, my_map, mini_way)
    # write_road(road_list)


# 测试用，计算拥挤度
def calculate_all_congestion(car_list, road_list, my_map, mini_way):
    cross_to_road = my_map.cross_to_road
    # 遍历车，求路径，并填充到road.history
    for car in car_list:
        mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
        curr_time = car.plan_time
        for i in range(1, mini_cross_path.__len__()):
            temp_road_id = cross_to_road[mini_cross_path[i - 1] - 1][mini_cross_path[i] - 1]
            temp_road = my_map.road_dic[temp_road_id]
            t = math.ceil(temp_road.length / min(car.speed, temp_road.speed))
            for j in range(t):
                if temp_road.history.get(curr_time + j) is None:
                    temp_road.history[curr_time + j] = 1
                else:
                    temp_road.history[curr_time + j] += 1
            curr_time += t - 1
    # 遍历路，计算并赋值拥堵程度
    sum = 0
    for road in road_list:
        sum += road.calculate_congestion()
    return sum / road_list.__len__()


# 测试分区效果
def partition(car_list):
    with open('../../logs/cars.log', 'w') as file:
        file.seek(0)
        file.truncate()
        D = [[0] * 4 for _ in range(4)]
        for car in car_list:
            file.write("%d to %d \n" % (car.from_cross.zone, car.to_cross.zone))
            if car.from_cross.zone == car.to_cross.zone:
                D[car.from_cross.zone][car.to_cross.zone] += 1
            else:
                D[car.from_cross.zone][car.to_cross.zone] += 1
                D[car.to_cross.zone][car.from_cross.zone] += 1
        file.write("Transaction Matrix:\n")
        for i in range(4):
            for j in range(4):
                file.write("%d " % D[i][j])
            file.write('\n')


# 写行车路径矩阵
def write_route(car_list, cross_num):
    with open('../../logs/route.log', 'w') as file:
        file.seek(0)
        file.truncate()
        D = [[0] * cross_num for _ in range(cross_num)]
        for car in car_list:
            file.write("%d:%d to %d \n" % (car.id, car.fro, car.to))
            D[car.fro - 1][car.to - 1] += 1
            D[car.to - 1][car.fro - 1] += 1
        file.write("Transaction Matrix:\n")
        file.write("   ")
        for j in range(cross_num):
            file.write("%4d" % (j + 1))
        file.write("\n")
        for i in range(cross_num):
            file.write("%3d:" % (i + 1))
            for j in range(cross_num):
                file.write("%3d " % D[i][j])
            file.write('\n')


# 将结果写入答案文件
def write_result(answer_path, car_list, my_map, mini_way):
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        temp = car_list[0].speed
        cross_to_road = my_map.cross_to_road
        for car in car_list:
            mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
            mini_road_path = ""
            # curr_time = car.plan_time
            # bias = math.floor((car.id - 10000) / 120) * 12
            for i in range(1, mini_cross_path.__len__()):
                temp_road_id = cross_to_road[mini_cross_path[i - 1] - 1][mini_cross_path[i] - 1]
                mini_road_path += "%d," % temp_road_id
                # temp_road = map.road_dic[temp_road_id]
                # t = math.ceil(temp_road.length / min(car.speed, temp_road.speed))
                # for j in range(t):
                #     if temp_road.history.get(curr_time + j + bias) is None:
                #         temp_road.history[curr_time + j + bias] = 1
                #     else:
                #         temp_road.history[curr_time + j + bias] += 1
                # curr_time += t - 1
            file.write('(%d,%d,%s)\n' % (
                    car.id, car.plan_time + (math.floor(car.sort_to_go / 120) * 10), mini_road_path[:-1]))


# 将结果写入答案文件 version2
def write_result_v2(answer_path, my_map, mini_way):
    car_list_v2 = my_map.car_list_v2
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        for j in range(2):
            cross_to_road = my_map.cross_to_road
            for car in car_list_v2[j]:
                bias = math.floor((car.id - 10000) / 140) * 10
                mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
                mini_road_path = ""
                for i in range(1, mini_cross_path.__len__()):
                    temp_road_id = cross_to_road[mini_cross_path[i - 1] - 1][mini_cross_path[i] - 1]
                    mini_road_path += "%d," % temp_road_id
                file.write('(%d,%d,%s)\n' % (car.id, car.plan_time + bias, mini_road_path[:-1]))


# 写路统计数据到文件
def write_road(road_list):
    with open('../../logs/roads.log', 'w') as file:
        file.seek(0)
        file.truncate()
        for road in road_list:
            file.write("{%d}[%d]" % (road.id, road.congestion))
            dic_str = ""
            # max_value = 0
            for key, value in road.history.items():
                dic_str += '%d:%d,' % (key, value)
                # max_value = max_value if max_value > value else value
            file.write('%s\n' % (dic_str))


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
