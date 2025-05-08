# tsp_project/tsp_solver.py
from distance import haversine

def compute_distance_matrix(places):
    n = len(places)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist[i][j] = haversine(places[i].lat, places[i].lon, places[j].lat, places[j].lon)
    return dist

def greedy_tsp(dist, start=0):
    n = len(dist)
    visited = [False] * n
    path = [start]
    visited[start] = True
    current = start

    for _ in range(n - 1):
        next_city = min((j for j in range(n) if not visited[j]), key=lambda j: dist[current][j])
        visited[next_city] = True
        path.append(next_city)
        current = next_city

    return path

def two_opt(path, dist):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path)):
                if j - i == 1:
                    continue
                new_path = path[:i] + path[i:j][::-1] + path[j:]
                if total_distance(new_path, dist) < total_distance(path, dist):
                    path = new_path
                    improved = True
    return path

def total_distance(path, dist):
    return sum(dist[path[i]][path[i + 1]] for i in range(len(path) - 1))
