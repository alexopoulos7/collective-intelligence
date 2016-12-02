from cluster import BiCluster
from utilities import pearson_distance


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
    clusters = [BiCluster(rows[i], id=i) for i in range(len(rows))]

    while len(clusters) > 1:
        print 'Loop with length of clusters = {}'.format(len(clusters))
        lowest_pair = (0, 1)
        closest = distance(clusters[0].vec, clusters[1].vec)
        print 'Closest distance so far is {}'.format(closest)
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
                    print 'Found lowest distance between i={} and j={} is ={}'.format(i, j, closest)

        # Calculate the average of the 2 clusters
        merged_clusters = [
            (clusters[lowest_pair[0]].vec[i] + clusters[lowest_pair[1]].vec[i]) / 2.0 for i in
            range(len(clusters[0].vec))
            ]
        print 'Lets create the new Merged Cluster id = {} between {} and {}'.format(current_cluster_id, lowest_pair[0],
                                                                                    lowest_pair[1])
        # Create the new cluster
        new_cluster = BiCluster(merged_clusters, left=clusters[lowest_pair[0]], right=clusters[lowest_pair[1]],
                                distance=closest, id=current_cluster_id)
        print 'New Clusters Left is {} '.format(new_cluster)

        # cluster ids that were not in the original set are negative
        current_cluster_id -= 1
        del clusters[lowest_pair[1]]
        del clusters[lowest_pair[0]]
        clusters.append(new_cluster)
    return clusters[0]

