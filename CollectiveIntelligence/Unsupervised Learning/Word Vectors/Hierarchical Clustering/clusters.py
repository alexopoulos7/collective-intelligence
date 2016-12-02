from math import sqrt
from cluster import BiCluster


def pearson_distance(v1, v2):
    """
    Calculate Pearson Distance between v1 and v2
    :param v1:
    :param v2:
    :return: float [0,1]. In this case we get close to 0 if items are similar
    """
    # Simple Sums
    sum1 = sum(v1)
    sum2 = sum(v2)
    min_length = min(len(v1), len(v2))

    # Sum of the squares
    sum1_square = sum([pow(v, 2) for v in v1])
    sum2_square = sum([pow(v, 2) for v in v2])

    # sum of the products
    product_sum = sum([v1[i] * v2[i] for i in range(min_length)])

    # Calculate Pearson Score
    num = product_sum - (sum1 * sum2 / len(v1))
    den = sqrt((sum1_square - pow(sum1, 2) / min_length) * (sum2_square - pow(sum2, 2) / min_length))
    if den == 0:
        return 1

    return 1.0 - num / den


def read_file(filename):
    """
    Load file with word counts.
    In this file columns are words and each row represents each blog and count of words
    :param filename:
    :return: a tuple of row names, column names and actual data
    """

    lines = [line for line in file(filename)]  # Use list complrehension to load lines from file

    # First line is the column of titles or word names
    column_names = lines[0].strip().split('\t')[1:]
    row_names = []
    data = []
    for line in lines[1:]:
        p = line.strip().split('\t')
        # First column in each row is the rowname (or name of blogs)
        print p[0]
        row_names.append(p[0])
        # The data for this row is the remainder of the row
        # data.append([float(x) for x in p[1:]])
        list_to_add = [float(x) for x in p[1:]]
        print 'Add to our data list with length {}'.format(len(list_to_add))
        data.append(list_to_add)
    return column_names, row_names, data


def hierarchical_cluster(rows, distance=pearson_distance):
    """
    Create Hierarchical Cluster groups.
    This algorithm begins by creating a group of clusters that are just the original items
    The main loop of the function searches for the 2 best matches by trying every possible pair and calculating their correlation distance.
    The best pair of clusters is merged into a single cluster.
    The data for this new cluster is the average of the 2 old clusters.
    The process is repeated until only one cluster remains.
    :param rows:
    :param distance:
    :return:
    """
    distances = {}
    current_cluster_id = -1

    # Clusters are initially just the rows
    clusters = [BiCluster(rows[i], id=1) for i in range(len(rows))]

    while len(clusters) > 1:
        lowest_pair = (0, 1)
        closest = distance(clusters[0].vec, clusters[1].vec)

        # Loop through every pair looking for the smallest distance
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # distances is the cache of distance calculations
                if (clusters[i].id, clusters[j].id) not in distances:
                    distances[(clusters[i].id, clusters[j].id)] = distance(clusters[i].vec, clusters[j].vec)

                d = distances[(clusters[i].id, clusters[j].id)]

                if d < closest:
                    closest = d
                    lowest_pair = (i, j)

            # Calculate the average of the 2 clusters
            merged_clusters = [
                (clusters[lowest_pair[0]].vec[i] + clusters[lowest_pair[1]].vec[i]) / 2.0 for i in
                range(len(clusters[0].vec))
                ]

            # Create the new cluster
            new_cluster = BiCluster(merged_clusters, left=clusters[lowest_pair[0]], right=clusters[lowest_pair[1]],
                                    distance=closest, id=current_cluster_id)

            # cluster ids the were not in the original set are negative
            current_cluster_id -= 1
            del clusters[lowest_pair[1]]
            del clusters[lowest_pair[0]]
            clusters.append(new_cluster)
        return clusters[0]


def print_clusters(clusters, labels=None, n=0):
    """
    Print Clusters tree recursively
    :param clusters:
    :param labels:
    :param n:
    :return:
    """

    # indent to make hierarchy layout
    for i in range(n):
        print '  '
        if clusters.id <0:
            # negative ids mean that this is branch
            print '-'
        else:
            # positive ids means that this is Endpoint
            if labels is None:
                print clusters.id
            else:
                print labels[clusters.id]
    # Now Print the Right and Left Branches
    print_clusters(clusters.left, labels=labels, n=n + 1)
    print_clusters(clusters.right, labels=labels, n=n + 1)




if __name__ == '__main__':
    cols, rows, data = read_file('../blogdata.txt')
    clusters = hierarchical_cluster(data)
    print clusters
