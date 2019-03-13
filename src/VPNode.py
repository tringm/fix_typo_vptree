import heapq


class VPNode:
    def __init__(self, lower_bounds=[], upper_bounds=[], children=[]):
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.children = children
        self.vantage_point = None

    def minimum_distance(self, distances):
        minimum = 0.0
        for i in range(len(distances)):
            if distances[i] < self.lower_bounds[i]:
                minimum = max(minimum, self.lower_bounds[i] - distances[i])
            elif distances[i] > self.upper_bounds[i]:
                minimum = max(minimum, distances[i] - self.upper_bounds[i])
        return minimum

    def search(self, item, distances, heap, distance_function):
        d = distance_function(self.vantage_point, item)
        new_distances = distances + (d,)

        heapq.heappush(heap, (d, 0, self.vantage_point))

        for child in self.children:
            heapq.heappush(heap, (child.minimum_distance(new_distances), 1, child, new_distances))
