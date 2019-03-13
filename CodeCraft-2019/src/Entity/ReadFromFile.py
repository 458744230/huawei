import Car
import Cross
import Road

def read(tag):
    path = "../" + tag + "/"
    carDict = []
    with open(path + "car.txt", "r") as carFile:
        for line in carFile.readlines():
            if line[0] != '#':
                carDict.append(Car.Car(line[1:-1].split(',')))
    crossDict = []
    with open(path + "cross.txt", "r") as crossFile:
        for line in crossFile.readlines():
            if line[0] != '#':
                crossDict.append(Cross.Cross(line[1:-1].split(',')))
    roadDict = []
    with open(path + "road.txt", "r") as roadFile:
        for line in roadFile.readlines():
            if line[0] != '#':
                roadDict.append(Road.Road(line[1:-1].split(',')))

    return carDict, crossDict, roadDict
