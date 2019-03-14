import Car
import Cross
import Road

def read(tag):
    path = "../" + tag + "/"
    carlist = []
    with open(path + "car.txt", "r") as carFile:
        for line in carFile.readlines():
            if line[0] != '#':
                carlist.append(Car.Car(parser(line)))
    crosslist = []
    with open(path + "cross.txt", "r") as crossFile:
        for line in crossFile.readlines():
            if line[0] != '#':
                crosslist.append(Cross.Cross(parser(line)))
    roadlist = []
    with open(path + "road.txt", "r") as roadFile:
        for line in roadFile.readlines():
            if line[0] != '#':
                roadlist.append(Road.Road(parser(line)))

    return carlist, crosslist, roadlist

def parser(str):
    str = str[str.find('(') + 1:str.find(')')]
    return str.split(',')