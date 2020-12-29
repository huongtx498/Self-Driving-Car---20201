import math
import pickle
from io import StringIO

import numpy


class DijkstraSPF(object):
    def __init__(self, G, s):
        """ Calculate shortest path from s to other nodes in G. """
        self.__dist = dist = dict()
        self.__prev = prev = dict()
        visited = set()
        queue = set()

        dist[s] = 0
        prev[s] = s
        queue.add(s)

        while queue:
            u = min(queue, key=dist.get)
            for v in self.get_adjacent_nodes(G, u):
                if v in visited:
                    continue
                alt = self.get_distance(u) + self.get_edge_weight(G, u, v)
                if alt < self.get_distance(v):
                    dist[v] = alt
                    prev[v] = u
                    queue.add(v)
            queue.remove(u)
            visited.add(u)

    @staticmethod
    def get_adjacent_nodes(G, u):
        return G.get_adjacent_nodes(u)

    @staticmethod
    def get_edge_weight(G, u, v):
        return G.get_edge_weight(u, v)

    def get_distance(self, u):
        """ Return the length of shortest path from s to u. """
        return self.__dist.get(u, math.inf)

    def get_path(self, v):
        """ Return the shortest path to v. """
        path = [v]
        while self.__prev[v] != v:
            v = self.__prev[v]
            path.append(v)
        return path[::-1]


class Graph(object):
    def __init__(self, adjacency_list=dict(), edge_weights=dict()):
        self.__adjacency_list = adjacency_list.copy()
        self.__edge_weights = edge_weights.copy()

    def add_edge(self, u, v, w):
        """ Add a new edge u -> v to graph with edge weight w. """
        self.__edge_weights[u, v] = w
        if u not in self.__adjacency_list:
            self.__adjacency_list[u] = set()
        self.__adjacency_list[u].add(v)

    def get_edge_weight(self, u, v):
        """ Get edge weight of edge between u and v. """
        return self.__edge_weights[u, v]

    def get_adjacent_nodes(self, u):
        """ Get nodes adjacent to u. """
        return self.__adjacency_list.get(u, set())

    def get_number_of_nodes(self):
        """ Return the total number of nodes in graph. """
        return len(self.__adjacency_list)

    def get_nodes(self):
        """ Return all nodes in this graph. """
        return self.__adjacency_list.keys()

    def __str__(self):
        io = StringIO()
        N = self.get_number_of_nodes()
        print("Directed, acyclic graph with %d nodes" % N, file=io)
        for u in self.get_nodes():
            adj = self.get_adjacent_nodes(u)
            print("Node %s: connected to %d nodes" % (u, len(adj)), file=io)
        return io.getvalue()


def get_path(start, end):
    # adj_mx, coor = pickle.load(open("/home/jackwiliams/Documents/Fuzzy/Self-Driving-Car---20201/fuzzy_base/point.p", "rb"))
    adj_mx, coor = pickle.load(open(
        "../fuzzy_base/point.p", "rb"))
    adj_mx[42, 57] = 0
    print(adj_mx[42, 57])
    graph = Graph()
    for i, a in enumerate(adj_mx):
        for j, b in enumerate(a):
            if b == 1:
                distance = numpy.linalg.norm(
                    numpy.array(coor[i + 1]) - numpy.array(coor[j + 1])
                )
                graph.add_edge(i + 1, j + 1, distance)
                graph.add_edge(j + 1, i + 1, distance)

    dijkstra = DijkstraSPF(graph, start)
    return dijkstra.get_path(end), dijkstra.get_distance(end)


get_path(11, 55)
