# -----coding:utf-8------
from Entity.Car import Car
from Entity.Cross import Cross
from Entity.Road import Road


def read(carpath, crosspath, roadpath):
    # path = "../" + tag + "/"
    carlist = []
    with open(carpath, "r") as carFile:
        for line in carFile.readlines():
            if line[0] != '#':
                carlist.append(Car(parser(line)))
    crosslist = []
    with open(crosspath, "r") as crossFile:
        for line in crossFile.readlines():
            if line[0] != '#':
                crosslist.append(Cross(parser(line)))
    roadlist = []
    with open(roadpath, "r") as roadFile:
        for line in roadFile.readlines():
            if line[0] != '#':
                roadlist.append(Road(parser(line)))

    return carlist, crosslist, roadlist


def parser(str):
    str = str[str.find('(') + 1:str.find(')')]
    return str.split(',')
