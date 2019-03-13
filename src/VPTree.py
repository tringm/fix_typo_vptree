import random
from src.VPNode import VPNode
import heapq
import numpy as np


def levenshtein_distance(word1, word2):
    len1 = len(word1)
    len2 = len(word2)
    if len1 > len2:
        word1, word2 = word2, word1
        len1, len2 = len2, len1

    current_row = range(len1 + 1)

    for i in range(1, len2 + 1):
        previous_row = current_row
        current_row = [i] + [0] * len1
        for j in range(1, len1 + 1):
            add_cost = previous_row[j] + 1
            delete_cost = current_row[j - 1] + 1
            change_cost = previous_row[j - 1]
            if word1[j - 1] != word2[i - 1]:
                change_cost += 1
            current_row[j] = min(add_cost, delete_cost, change_cost)
    return current_row[len1]


class VPTree:
    def __init__(self, items, counter, distance_function=levenshtein_distance):
        self.counter = counter
        self.left = None
        self.right = None
        self.left_min = np.inf
        self.left_max = 0
        self.right_min = np.inf
        self.right_max = 0
        self.distance_function = distance_function

        self.vantage_point = items[0]

        items = items[1:]

        distances = [self.distance_function(self.vantage_point, item) for item in items]

        items_sorted_by_distance = sorted(zip(items, distances), key=lambda x: x[1], reverse=True)

        median_pos = len(items) // 2 + 1

        right_items = [packed[0] for packed in items_sorted_by_distance[:median_pos]]
        if len(right_items) > 0:
            self.right_min = items_sorted_by_distance[median_pos - 1][1]
            self.right_max = items_sorted_by_distance[0][1]
            self.right = VPTree(right_items, self.counter, distance_function)

        left_items = [packed[0] for packed in items_sorted_by_distance[median_pos:]]
        if len(left_items) > 0:
            self.left_min = items_sorted_by_distance[len(items_sorted_by_distance) - 1][1]
            self.left_max = items_sorted_by_distance[median_pos][1]
            self.left = VPTree(left_items, self.counter, distance_function)

    def __lt__(self, other):
        return self.counter[self.vantage_point] < other.counter[self.vantage_point]

    def is_leaf(self):
        return (self.left is None) and (self.right is None)

    def knn(self, item, k):
        heap = []
        heapq.heappush(heap, (0, self))

        furthest_d = np.inf

        neighbors = []

        while heap:
            d0, node = heapq.heappop(heap)
            if node is None or d0 > furthest_d:
                continue

            d = self.distance_function(item, node.vantage_point)
            if d <= furthest_d:
                heapq.heappush(neighbors, (d, node.vantage_point))
                furthest_d = d

            if node.is_leaf():
                continue

            if node.left_min <= d <= node.left_max:
                heapq.heappush(heap, (0, node.left))
            elif node.left_min - furthest_d <= d <= node.left_max + furthest_d:
                heapq.heappush(heap, (node.left_min - d if d < node.left_min else d - node.left_max, node.left))

            if node.right_min <= d <= node.right_max:
                heapq.heappush(heap, (0, node.right))
            elif node.right_min - furthest_d <= d <= node.right_max + furthest_d:
                heapq.heappush(heap, (node.right_min - d if d < node.right_min else d - node.right_max, node.right))

        return heapq.nsmallest(k, neighbors)











# class VPTree:
#     def __init__(self, items, max_children=2, distance_function=levenshtein_distance):
#         """
#         :param items: List of items(words) to be put into this VPTree
#         :param distance_function: function for calculate distance between word (default = Levenshtein
#         :param max_children:
#         """
#         """ items        : list of items to make tree out of
#             distance     : function that returns the distance between two items
#             max_children : maximum number of children for each node
#
#             Using larger max_children will reduce the time needed to construct the tree,
#             but may make queries less efficient.
#         """
#
#         self.distance_function = distance_function
#         self.max_children = max_children
#         items = [(item, ()) for item in items]
#         random.shuffle(items)
#         self.root = build_node(items, self.distance_function, self.max_children)
#
#     def find(self, item):
#         """ Return iterator yielding items in tree in order of distance from supplied item.
#         """
#
#         if not self.root:
#             return
#
#         heap = [(0, 1, self.root, ())]
#
#         while heap:
#             top = heapq.heappop(heap)
#             if top[1]:
#                 top[2].search(item, top[3], heap, self.distance_function)
#             else:
#                 return top[2], top[0]
#
#
# def build_node(items, distance_function, max_children):
#     if not items:
#         return None
#
#     node = VPNode()
#     n_distance = len(items[0][1])
#     for i in range(n_distance):
#         distances = [item[1][i] for item in items]
#         node.lower_bounds.append(min(distances))
#         node.upper_bounds.append(max(distances))
#
#     node.vantage_point = items[0][0]
#     items = items[1:]
#
#     if not items:
#         return node
#
#     items = [(item[0], item[1] + (distance_function(node.vantage_point, item[0]),)) for item in items]
#
#     distances = sorted([item[1][-1] for item in items])
#     n_children = min(max_children, len(distances))
#     split_points = [-1]
#     for i in range(n_children):
#         split_points.append(distances[(i + 1) * (len(distances) - 1) // n_children])
#
#     for i in range(n_children):
#         child_items = [item for item in items if split_points[i] < item[1][-1] <= split_points[i + 1]]
#         child = build_node(child_items, distance_function, max_children)
#         if child:
#             node.children.append(child)
#     return node
