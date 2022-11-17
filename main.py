import copy
from itertools import permutations, groupby
import time


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


# Replaces costs with -1 value
def ignore_routes(graph, start_node, end_node, path):
    for line_index in range(len(graph)):
        if line_index == start_node:
            for node_index in range(len(graph[line_index])):
                graph[line_index][node_index] = -1
        graph[line_index][end_node] = -1
    graph[end_node][start_node] = -1

    # Remove costs of routes connecting previously visited nodes with current one
    for node in path:
        graph[end_node][node] = -1
    return graph


def explore_graph_level(data, initial_cost, start_node, nodes_to_visit, path, should_count_path_to_start_node):
    graph, cost = optimize_graph(data)
    costs_list = []
    graphs_copies = []

    for node in nodes_to_visit:
        copy_of_data = copy.deepcopy(data)
        copy_of_graph = ignore_routes(copy_of_data, start_node, node, path)
        copy_of_graph, cost_of_graph = optimize_graph(copy_of_graph)

        current_cost = initial_cost + cost_of_graph
        if graph[start_node][node] != -1:
            current_cost += graph[start_node][node]

        costs_list.append(current_cost)
        graphs_copies.append(copy_of_graph)
    lowest_cost_node_index = costs_list.index(min(costs_list))
    path.append(nodes_to_visit[lowest_cost_node_index])

    if should_count_path_to_start_node:
        current_cost += data[0][nodes_to_visit[0]]
        path.append(0)

    nodes_to_visit.pop(lowest_cost_node_index)

    return lowest_cost_node_index, graphs_copies[lowest_cost_node_index], min(
        costs_list), nodes_to_visit, path, current_cost


def find_path(data, initial_cost):
    path = []
    should_count_path_to_start_node = False
    # Always start from 0
    start_node = 0
    path.append(0)

    nodes_to_visit = []
    for node in range(len(data[0])):
        nodes_to_visit.append(node)

    # Remove first node because we always start from the first
    nodes_to_visit.remove(0)

    # Find low cost node in first graph level
    start_node, graph_to_continue, lowest_cost, nodes_to_visit, path, total_cost = explore_graph_level(data,
                                                                                                       initial_cost,
                                                                                                       start_node,
                                                                                                       nodes_to_visit,
                                                                                                       path,
                                                                                                       should_count_path_to_start_node)

    while len(nodes_to_visit) > 0:
        if len(nodes_to_visit) == 1:
            should_count_path_to_start_node = True
        next_node_to_check, graph_to_continue, lowest_cost, nodes_to_visit, path, total_cost = explore_graph_level(
            graph_to_continue,
            lowest_cost,
            start_node + 1,
            nodes_to_visit,
            path,
            should_count_path_to_start_node)
        start_node = next_node_to_check

    return lowest_cost, path


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

        if file_name == "tsp_6_1.txt" or file_name == "tsp_6_2.txt":
            for test in range(number_of_tests):
                ten_repetitions_time = 0
                for repetition in range(20):
                    start = time.time_ns()

                    optimized_graph, cost_of_graph = optimize_graph(load_graph("TestData/" + file_name))
                    counted_min_path_weight, counted_path = find_path(optimized_graph, cost_of_graph)
                    if counted_min_path_weight == min_path_weight:
                        print("Good job, that's right.")
                    else:
                        # print("The algorithm is wrong. Check the minimal path weight.")
                        pass

                    if counted_path == min_path:
                        print("Good job, that's right.")
                    else:
                        print("The algorithm is wrong. Check the minimal path")
                    print("Counted path:")
                    print(counted_path)
                    print("Counted cost:")
                    print(counted_min_path_weight)

                    end = time.time_ns()
                    ten_repetitions_time += end - start
                operation_time = ten_repetitions_time / 20
                output_file.write(str(operation_time) + "\n")
        else:
            for test in range(number_of_tests):
                operation_time = 0
                start = time.time_ns()

                optimized_graph, cost_of_graph = optimize_graph(load_graph("TestData/" + file_name))
                counted_min_path_weight, counted_path = find_path(optimized_graph, cost_of_graph)

                if counted_min_path_weight == min_path_weight:
                    print("Good job, that's right.")
                else:
                    print("The algorithm is wrong. Check the minimal path weight.")

                if counted_path == min_path:
                    print("Good job, that's right.")
                else:
                    print("The algorithm is wrong. Check the minimal path")
                print("Counted path:")
                print(counted_path)
                print("Counted cost:")
                print(counted_min_path_weight)

                end = time.time_ns()
                operation_time += end - start
                output_file.write(str(operation_time) + "\n")
    output_file.write(configuration[len(configuration) - 1])
    output_file.close()


if __name__ == "__main__":
    configuration = load_initialization_file("init.ini")
    test_algorithm(configuration)
