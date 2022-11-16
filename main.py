import copy
from itertools import permutations, groupby
import time
import numpy as np


# Load matrix of path costs from txt data file
def load_graph(filename):
    datafile = open(filename, "r")
    lines = datafile.read().splitlines()
    matrix = []
    for i in range(1, len(lines)):
        matrix.append(list(map(int, lines[i].split())))
    datafile.close()
    return matrix


def get_number_of_cities(filename):
    datafile = open(filename, "r")
    return datafile.readline()


# Returns the permutation of nodes
def get_permutation(start_node, number_of_cities):
    nodes = []
    for node in range(int(number_of_cities)):
        if node != start_node:
            nodes.append(node)
    return permutations(nodes)


def ignore_routes(graph, start_node, end_node):
    for line_index in range(len(graph)):
        if line_index == start_node:
            for node_index in range(len(graph[line_index])):
                graph[line_index][node_index] = -1
        graph[line_index][end_node] = -1
    graph[end_node][start_node] = -1
    return graph


def explore_graph_level(data, number_of_cities, initial_cost, start_node, nodes_to_visit):
    number_of_cities = int(number_of_cities)
    graph, cost = optimize_graph(data)
    # nodes_to_visit = []
    costs_list = []
    nodes_list = []
    graphs_copies = []

    # for node in range(len(data[0])):
    #     nodes_to_visit.append(node)
    # nodes_to_visit.remove(0)
    nodes_to_visit.remove(start_node)

    # for node in range(1, number_of_cities):
    # TODO ostatnia zmiana
    for node in nodes_to_visit:
        copy_of_data = copy.deepcopy(data)
        copy_of_graph = ignore_routes(copy_of_data, start_node, node)
        # to jest z 4, teraz trzeba nalozyc ograniczenia i uzyskac to co w 2 rzedzie
        # 4 wiersz i 2 kolumnne trzeba wywalic
        copy_of_graph, cost_of_graph = optimize_graph(copy_of_graph)
        a = graph[start_node][node]
        b = initial_cost
        c = cost_of_graph
        current_cost = a + b + c
        costs_list.append(current_cost)
        nodes_list.append(node)
        graphs_copies.append(copy_of_graph)
    lowest_cost_node_to_continue = nodes_list[costs_list.index(min(costs_list)) - 1]
    # TODO
    a = lowest_cost_node_to_continue
    return lowest_cost_node_to_continue, graphs_copies[lowest_cost_node_to_continue], min(costs_list)


def find_path(data, number_of_cities, initial_cost):
    graph_to_continue = []
    start_node = 0

    nodes_to_visit = []
    for node in range(len(data[0])):
        nodes_to_visit.append(node)



    # find low cost node in first graph level
    node_index_to_continue, graph_to_continue, lowest_cost = explore_graph_level(data, number_of_cities, initial_cost,
                                                                                 start_node, nodes_to_visit)

    next_node_to_check, graph_to_continue, lowest_cost = explore_graph_level(graph_to_continue, number_of_cities,
                                                                             lowest_cost, node_index_to_continue + 1,
                                                                             nodes_to_visit)
    while node_index_to_continue != 0:  # TODO nie wiem czy taki warunek
        next_node_to_check, graph_to_continue, lowest_cost = explore_graph_level(graph_to_continue, number_of_cities,
                                                                                 lowest_cost, start_node + 1,
                                                                                 nodes_to_visit)
        start_node = next_node_to_check

    # # Initialize min_path as maximal int size
    # min_path = 2147483647
    # # Initialize path as list for vertices
    # path = []
    # # Assume that we always start from the first node
    # options = get_permutation(0, number_of_cities)
    # for route in options:
    #     weight = 0
    #     i = 0
    #     for vertex in route:
    #         weight += int(data[i][vertex])
    #         i = vertex
    #     # Assume that we always start from the first node
    #     weight += int(data[i][0])
    #     if weight < min_path:
    #         min_path = weight
    #         path = list(route)
    #         path.insert(0, 0)
    #         path.append(0)
    #############################################################################
    # DF = DepthFirstSearch(graph, number_of_cities)
    #
    # # start = time.time()
    # DF.DepthFirsIterative(0)
    # # end = time.time()
    # #
    # # print('\nCzas egzekucji: ', end - start, 'segundos.\n')
    #
    # path = showPath(DF)
    # print('\nsposób rozwiązanie: ', path)
    # print('\nCosto total: ', DF.lowerCost)
    return 0, "0"


def load_initialization_file(filename):
    init_file = open(filename, "r")
    configuration = init_file.read().splitlines()
    init_file.close()
    return configuration


def second_lowest_cost(list):
    g = groupby(list)
    if next(g, True) and not next(g, False):
        return 0
    else:
        return sorted(set(list))[1]


def optimize_graph(data):
    graph = copy.deepcopy(data)
    cost_of_graph = 0
    nodes = len(graph[0])

    # optimize rows
    for line in graph:
        lowest_cost = second_lowest_cost(line)
        for i in range(nodes):
            if line[i] != -1:
                line[i] -= lowest_cost
        cost_of_graph += lowest_cost

    # optimize columns
    for i in range(nodes):
        column = []
        for line in graph:
            column.append(line[i])
        lowest_column_cost = second_lowest_cost(column)
        if 0 not in column:
            cost_of_graph += lowest_column_cost
            for line in graph:
                if line[i] != -1:
                    line[i] -= lowest_column_cost
    # print(graph)
    return graph, cost_of_graph


def test_algorithm(configuration):
    output_file = open(configuration[len(configuration) - 1], "w")
    for testing_case in range(len(configuration) - 1):
        output_file.write(configuration[testing_case] + "\n")
        testing_case_data = configuration[testing_case].split()
        file_name = testing_case_data[0]
        number_of_tests = int(testing_case_data[1])
        min_path_weight = int(testing_case_data[2])
        min_path = list(map(int, configuration[testing_case].split("[")[1].split(']')[0].split()))

        # TODO
        if file_name == "tsp_6_1.txt" or file_name == "tsp_6_2.txt" or file_name == "hindus.txt":
            for test in range(number_of_tests):
                ten_repetitions_time = 0
                for repetition in range(20):
                    start = time.time_ns()

                    optimized_graph, cost_of_graph = optimize_graph(load_graph("TestData/" + file_name))
                    counted_min_path_weight, counted_path = find_path(optimized_graph,
                                                                      get_number_of_cities("TestData/" + file_name),
                                                                      cost_of_graph)
                    if counted_min_path_weight == min_path_weight:
                        print("Good job, that's right.")
                    else:
                        print("The algorithm is wrong. Check the minimal path weight.")

                    if counted_path == min_path:
                        print("Good job, that's right.")
                    else:
                        print("The algorithm is wrong. Check the minimal path")

                    end = time.time_ns()
                    ten_repetitions_time += end - start
                operation_time = ten_repetitions_time / 20
                output_file.write(str(operation_time) + "\n")
        else:
            for test in range(number_of_tests):
                operation_time = 0
                start = time.time_ns()

                optimized_graph, cost_of_graph = optimize_graph(load_graph("TestData/" + file_name))
                counted_min_path_weight, counted_path = find_path(optimized_graph,
                                                                  get_number_of_cities("TestData/" + file_name),
                                                                  cost_of_graph)

                if counted_min_path_weight == min_path_weight:
                    print("Good job, that's right.")
                else:
                    print("The algorithm is wrong. Check the minimal path weight.")

                if counted_path == min_path:
                    print("Good job, that's right.")
                else:
                    print("The algorithm is wrong. Check the minimal path")

                end = time.time_ns()
                operation_time += end - start
                output_file.write(str(operation_time) + "\n")
    output_file.write(configuration[len(configuration) - 1])
    output_file.close()


# def showPath(depthFirstObj):
#     pathStr = '[0]'
#     bestSolution = depthFirstObj.solutionsArr[depthFirstObj.bestSolution]
#     for i in range(0, len(bestSolution) - 1):
#         row = bestSolution[i]
#         col = bestSolution[i + 1]
#         pathStr = pathStr + ' -> ' + str(depthFirstObj.graph[row, col]) + ' -> [' + str(bestSolution[i + 1]) + ']'
#     return pathStr


if __name__ == "__main__":
    configuration = load_initialization_file("init.ini")
    test_algorithm(configuration)
