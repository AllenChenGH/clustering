from collections import defaultdict
from math import inf
import random
import csv


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """
    element_number = len(points)
    dimension_number = len(points[0])
    center = []

    for i in range(dimension_number):
        center.append(0)

    for i in range(element_number):
        for j in range(dimension_number):
            center[j] = center[j] + points[i][j]

    for i in range(dimension_number):
        center[i] = center[i]/element_number

    return center


def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """
    element_number = len(data_set)
    centers = []

    max = 0
    for assignment in assignments:
        if (assignment > max):
            max = assignment

    for i in range(max + 1):
        points = []
        for j in range(element_number):
            if (assignments[j] == i):
                points.append(data_set[j])
        centers.append(point_avg(points))

    return centers


def assign_points(data_points, centers):
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    dist = 0
    dimension = len(a)

    for i in range(dimension):
        dist = dist + (a[i] - b[i]) * (a[i] - b[i])

    return dist


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    element_number = len(data_set)
    centers = []
    random_list = []

    if k > element_number - 1:
        raise ValueError("k >= n!")

    for i in range(k):
        while True:
            temp = random.randint(0, element_number - 1)
            if temp not in random_list:
                random_list.append(temp)
                break

    for i in random_list:
        centers.append(data_set[i])

    return centers


def get_list_from_dataset_file(dataset_file):
    file = open(dataset_file, "r")
    reader = csv.reader(file)
    data = []

    for i in reader:
        temp = []
        temp.append(float(i[0]))
        temp.append(float(i[1]))
        data.append(temp)

    return data


def cost_function(clustering):
    cost = 0

    for label in clustering:
        points = []
        for point in clustering[label]:
            points.append(point)
        center = point_avg(points)
        for point in clustering[label]:
            cost = cost+distance(center,point)

    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
