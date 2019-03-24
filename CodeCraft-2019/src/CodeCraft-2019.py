# -----coding:utf-8------
# import logging
import numpy as np
import sys
import Entity
import math
import random

np.set_printoptions(threshold=np.inf)

# logging.basicConfig(level=logging.DEBUG,
#                     filename='../../logs/CodeCraft-2019.log',
#                     format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S',
#                     filemode='a')


def main():
    if len(sys.argv) != 5:
        # logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    # logging.info("car_path is %s" % (car_path))
    # logging.info("road_path is %s" % (road_path))
    # logging.info("cross_path is %s" % (cross_path))
    # logging.info("answer_path is %s" % (answer_path))

    car_list, cross_list, road_list = Entity.read(car_path, cross_path, road_path)
    # write_route(car_list,cross_list.__len__())
    # car_list.sort(key=lambda x: x.speed, reverse=True)
    mini_way = Entity.Min_way(road_list, cross_list.__len__(), 0)
    mini_way2 = Entity.Min_way(road_list, cross_list.__len__(), 1)
    my_map = Entity.Map(road_list, cross_list, car_list)
    my_map.partition()
    # my_map.plot()
    # for i in range(car_list.__len__()):
    #     car_list[i].sort_to_go = i + 1
    for j in range(2):
        for i in range(my_map.car_list_v2[j].__len__()):
            my_map.car_list_v2[j][i].sort_to_go = i + 1
    # write_result(answer_path, car_list, my_map, mini_way)
    write_result_v2(answer_path, my_map, mini_way, mini_way2)
    # write_result_v4(answer_path, my_map, mini_way, mini_way2)
    # calculate_all_congestion(car_list, road_list, my_map, mini_way)
    # write_road(road_list)
    # write_route(my_map, mini_way)
    # write_result_v3(answer_path,my_map,mini_way)

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
def write_route(my_map, mini_way):
    cross_num = my_map.cross_list.__len__()
    car_list = my_map.car_list
    with open('../../logs/route.log', 'w') as file:
        file.seek(0)
        file.truncate()

        D = [[[] for _ in range(cross_num)] for _ in range(cross_num)]
        R = [[{} for _ in range(cross_num)] for _ in range(cross_num)]
        for car in car_list:
            # file.write("%d:%d to %d \n" % (car.id, car.fro, car.to))
            D[car.fro - 1][car.to - 1].append(car)
        file.write("Transaction Matrix:\n")
        file.write("   ")
        for j in range(cross_num):
            file.write("%4d" % (j + 1))
        file.write("\n")
        for i in range(cross_num):
            file.write("%3d:" % (i + 1))
            for j in range(cross_num):
                file.write("%3d " % D[i][j].__len__())
            file.write('\n')
        road_dict = my_map.road_dict
        for i in range(cross_num):
            for j in range(cross_num):
                if D[i][j].__len__() > 0:
                    D[i][j].sort(key=lambda x: x.speed, reverse=True)
                    mini_path = mini_way.mini_road(i+1, j+1)
                    min_channel = 9999
                    total_time = 0
                    mini_road = ""
                    for road_id in mini_path:
                        mini_road += "%d," % road_id
                        now_road = road_dict.get(road_id)
                        min_channel = min_channel if now_road.channel > min_channel else now_road.channel
                        total_time += now_road.get_min_time()  # 粗略计算
                    send_rate = min(road_dict.get(mini_path[0]).speed, D[i][j][-1].speed) * min_channel
                    total_time += D[i][j].__len__() / send_rate
                    file.write("%d to %d: %d (%s)\n" % (i, j, total_time, mini_road[:-1]))


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
def write_result_v2(answer_path, my_map, mini_way, mini_way2):
    car_list_v2 = my_map.car_list_v2
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        for j in range(2):
            # cross_to_road = my_map.cross_to_road
            for car in car_list_v2[j]:
                # mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
                mini_road_path = None
                choose = random.randint(0, 1)
                if choose == 0:
                    mini_road_path = mini_way.mini_road(car.fro, car.to)
                else:
                    mini_road_path = mini_way2.mini_road(car.fro, car.to)
                mini_road = ""
                bias = (math.floor(car.sort_to_go / 75) * 11)
                for road_id in mini_road_path:
                    mini_road += "%d," % road_id
                file.write('(%d,%d,%s)\n' % (car.id, car.plan_time + bias, mini_road[:-1]))


# 将结果写入答案文件 version3
def write_result_v3(answer_path, my_map, mini_way):
    car_list_v2 = my_map.car_list_v2
    cross_num = my_map.cross_list.__len__()
    road_dict = my_map.road_dict
    max_time = 10000
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        # 两种方向分开处理
        for j in range(2):
            D = [[[] for _ in range(cross_num)] for _ in range(cross_num)]
            R = {}
            for car in car_list_v2[j]:
                D[car.fro - 1][car.to - 1].append(car)
            valid_pair = [(i, j) for i in range(cross_num) for j in range(cross_num) if D[i][j].__len__() > 0]
            for pair in valid_pair:
                D[pair[0]][pair[1]].sort(key=lambda x: x.speed, reverse=True)
                mini_path = mini_way.mini_road(pair[0] + 1, pair[1] + 1)
                min_channel = 9999
                total_time = 0
                for road_id in mini_path:
                    now_road = road_dict.get(road_id)
                    min_channel = min_channel if now_road.channel > min_channel else now_road.channel
                    total_time += now_road.get_min_time()  # 粗略计算
                send_rate = min(road_dict.get(mini_path[0]).speed, D[pair[0]][pair[1]][-1].speed) * min_channel
                total_time += D[pair[0]][pair[1]].__len__() / send_rate
                R[pair] = {}
                R[pair]['path'] = mini_path
                R[pair]['total_time'] = math.floor(total_time)
                R[pair]['min_channel'] = min_channel
                R[pair]['send_rate'] = send_rate
            road_using_dict = {}
            for i in range(max_time):
                for k in list(road_using_dict):
                    road_using_dict[k] -= 1
                    if road_using_dict[k] <= 10:
                        road_using_dict.pop(k)
                for pair in valid_pair:
                    flag = 0
                    for road_id in R[pair]['path']:
                        if road_using_dict.get(road_id) is not None:
                            flag = 1
                            break
                    if flag == 1:  # 路被占用，不走
                        continue
                    total_time = R[pair]['total_time']
                    for road_id in R[pair]['path']:
                        road_using_dict[road_id] = total_time
                    mini_road = ""
                    for road_id in R[pair]['path']:
                        mini_road += "%d," % road_id
                    for car in D[pair[0]][pair[1]]:
                        file.write(('(%d,%d,%s)\n' % (car.id, i + car.plan_time, mini_road[:-1])))
                    valid_pair.remove(pair)
                if valid_pair.__len__() == 0:
                    break


# 将结果写入答案文件 version4
def write_result_v4(answer_path, my_map, mini_way, mini_way2):
    car_list_v2 = my_map.car_list_v2
    cross_num = my_map.cross_list.__len__()
    # road_dict = my_map.road_dict
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        # 两种方向分开处理
        for j in range(2):
            dispatch = Entity.Dispatch(car_list_v2[j], cross_num)
            # max_speed = dispatch.max_speed
            # min_speed = dispatch.min_speed
            span_size = 4
            for i in range(car_list_v2[j].__len__()):
                car = dispatch.pop()
                if 200 < span_size < 400:
                    span_size = 6
                elif 400 <= span_size < 600:
                    span_size = 9
                else:
                    span_size = 13
                mini_road_path = None
                choose = random.randint(0, 2)
                if choose == 0:
                    mini_road_path = mini_way.mini_road(car.fro, car.to)
                else:
                    mini_road_path = mini_way2.mini_road(car.fro, car.to)
                mini_road = ""
                bias = (math.floor(i / 75) * span_size)
                for road_id in mini_road_path:
                    mini_road += "%d," % road_id
                file.write('(%d,%d,%s)\n' % (car.id, car.plan_time + bias, mini_road[:-1]))


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
