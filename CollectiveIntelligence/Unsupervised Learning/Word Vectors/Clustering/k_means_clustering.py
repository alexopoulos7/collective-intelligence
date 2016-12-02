from utilities import pearson_distance
from random import random


def k_means_clustering(rows, distance=pearson_distance, k=4):
    """
    k-means clustering algorithm begins with k randomly placed centroids
    and assigns every item to the nearest one.
    After the assignment the centroids are moved to the average location of all the nodes
    assigned to them and the assignments are redone
    This process repeat until the assignments stop changing
    :param rows: Data
    :param distance: Distance Function
    :param k: how many clusters do you want to make
    :return:
    """
    # Determine the min and max values for each point
    ranges = [(min(row[i] for row in rows), max([row[i] for row in rows])) for i in range(len(rows[0]))]

    # Create k RANDOMLY placed centroids
    clusters = [[random() * (ranges[i][1] - ranges[i][0]) + ranges[i][0] for i in range(len(rows[0]))] for j in
                range(k)]

    last_matches = None
    best_matches = None
    for t in range(100):
        print ('Iteration {}'.format(t))
        best_matches = [[] for i in range(k)]

        # Find the centroid that is the closest for each row
        for j in range(len(rows)):
            row = rows[j]
            best_match = 0
            for i in range(k):
                d = distance(clusters[i], row)
                if d < distance(clusters[best_match], row):
                    best_match = i
            best_matches[best_match].append(j)

        # if the results are the same as last time, then this is complete
        if best_matches == last_matches:
            break
        last_matches = best_matches

        # Move the centroids to the average of their members
        for i in range(k):
            avgs = [0.0] * len(rows[0])
            if len(best_matches[i]) > 0:
                for row_id in best_matches[i]:
                    for m in range(len(rows[row_id])):
                        avgs[m] += rows[row_id][m]
                for j in range(len(avgs)):
                    avgs[j] /= len(best_matches[i])
                clusters[i] = avgs

    return best_matches
