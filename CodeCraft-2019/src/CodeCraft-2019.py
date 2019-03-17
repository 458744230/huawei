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
    mini_way = Entity.Min_way(road_list)
    map = Entity.Map(road_list, cross_list, car_list)

    calculate_all_congestion(car_list, road_list, map, mini_way)
    write_result(answer_path, car_list, road_list, map, mini_way)


def calculate_all_congestion(car_list, road_list, map, mini_way):
    cross_to_road = map.cross_to_road
    # 遍历车，求路径，并填充到road.history
    for car in car_list:
        mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
        curr_time = car.plan_time
        for i in range(1, mini_cross_path.__len__()):
            temp_road_id = cross_to_road[mini_cross_path[i - 1] - 1][mini_cross_path[i] - 1]
            temp_road = map.road_dic[temp_road_id]
            t = math.ceil(temp_road.length / min(car.speed, temp_road.speed))
            for j in range(t):
                if temp_road.history.get(curr_time + j) is None:
                    temp_road.history[curr_time + j] = 1
                else:
                    temp_road.history[curr_time + j] += 1
            curr_time += t - 1
    # 遍历路，计算并赋值拥堵程度
    for road in road_list:
        road.calculate_congestion()


def write_result(answer_path, car_list, road_list, map, mini_way):
    with open(answer_path, 'w') as file:
        file.seek(0)
        file.truncate()
        file.write('#(carId,StartTime,RoadId...)\n')
        cross_to_road = map.cross_to_road
        for car in car_list:
            mini_cross_path = mini_way.returnvisitpath(car.fro, car.to)
            mini_road_path = ""
            curr_time = car.plan_time
            for i in range(1, mini_cross_path.__len__()):
                temp_road_id = cross_to_road[mini_cross_path[i - 1] - 1][mini_cross_path[i] - 1]
                mini_road_path += "%d," % temp_road_id
                temp_road = map.road_dic[temp_road_id]
                t = math.ceil(temp_road.length / min(car.speed, temp_road.speed))
                for j in range(t):
                    if temp_road.history.get(curr_time + j) is None:
                        temp_road.history[curr_time + j] = 1
                    else:
                        temp_road.history[curr_time + j] += 1
                curr_time += t - 1
            file.write('(%d,%d,%s)\n' % (car.id, car.plan_time, mini_road_path[:-1]))

    with open('../../logs/roads.log', 'w') as file:
        file.seek(0)
        file.truncate()
        for road in road_list:
            file.write("{%d}[%d]\n" % (road.id, road.congestion))
            # dic_str = ""
            # max_value = 0
            # for key, value in road.history.items():
            #     dic_str += '%d:%d,' % (key, value)
            #     max_value = max_value if max_value > value else value
            # file.write('[%d]%s\n' % (max_value, dic_str))


# to read input file
# process
# to write output file


if __name__ == "__main__":
    main()
