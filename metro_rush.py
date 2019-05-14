from argparse import ArgumentParser
from sys import stderr
from re import match


class Node:

    def __init__(self, station_ID, interchange, limitation, station_name):
        self.station_ID = station_ID
        self.interchange = interchange
        self.limitation = limitation
        self.station_name = station_name


class Graph:

    def __init__(self, metrolines, start, end):
        self.nodes = set_nodes(metrolines, start, end)         # {line:{station:node}}
        self.start_node = self.nodes[start[0]][start[1]]
        self.end_node = self.nodes[end[0]][end[1]]

    def find_way():
        way = None
        return way


def get_station_data(limitation, metroline, station, start, end):
    interchange = [metroline]
    station_ID = station.split(":")[0]
    station_name = station.split(":")[1]
    if ":Conn:" in station:
        interchange += station.split(":Conn: ")[1:]
    if (metroline == start[0] and station_ID == start[1]) or (metroline == end[0] and station_ID == end[1]):
        limitation = False

    return station_ID, limitation, interchange, station_name


def set_nodes(metrolines, start, end):
    nodes = {}
    interchange = []
    for metroline in metrolines:
        for station in metrolines[metroline]:
            station_ID, limitation, interchange, station_name = get_station_data(True, metroline, station, start, end)
            node = Node(station_ID, limitation, interchange, station_name)
            if metroline not in nodes :
                nodes[metroline] = {station_ID: node}
            else:
                nodes[metroline].update({station_ID: node})
    return nodes


def get_metrolines(lines):
    metrolines = {}
    metroline = None
    for index, line in enumerate(lines):
        if line.startswith("#"):
            metroline = line.replace("#","")
            metrolines[metroline] = []
        elif not line.startswith("START=") and not line.startswith("END=") and not line.startswith("TRAINS") and line:
            metrolines[metroline].append(line)
    return metrolines


def get_data(lines):
    """
    Get start station, end station and train number

    Return start: tuple(station ID, metro line)
    Return end: tuple(station ID, metro line)
    Return trains_number: train number
    """
    try:
        for line in lines[::-1]:
            if match("START=(.*?):", line):
                metro_line = match("START=(.*?):", line).group(1)
                ID = line.replace("START=" + metro_line + ":","")
                start = (metro_line, ID)
            elif match("END=(.*?):", line):
                metro_line = match("END=(.*?):", line).group(1)
                ID = line.replace("END=" + metro_line + ":","")
                end = (metro_line, ID)
            elif line.startswith("TRAINS="):
                trains_number = line.replace("TRAINS=","")
        return start, end, trains_number
    except Exception as e:
        print("Invalid File", file = stderr)
        exit()


def read_file(file_name):
    try:
        open_file = open(file_name, "r")
        lines = open_file.read().splitlines()
        open_file.close()
        return lines
    except Exception:
        print("Error")
        exit()


def get_file_name():
    """
    Get the file name from user's input
    """
    parser = ArgumentParser()
    parser.add_argument('file_name', metavar='file_name')
    args = parser.parse_args()
    return args.file_name


def main():
    file_name = get_file_name()
    lines = read_file(file_name)
    start, end, trains_number = get_data(lines)
    metrolines = get_metrolines(lines)
    graph = Graph(metrolines, start, end)
    print(graph.nodes)


if __name__ == "__main__":
    main()
