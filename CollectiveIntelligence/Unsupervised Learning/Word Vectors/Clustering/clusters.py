from dendogram import draw_dendogram
from hierarchical_clustering import hierarchical_cluster


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
        # print 'Add to our data list with length {}'.format(len(list_to_add))
        data.append(list_to_add)
    return row_names, column_names, data


def print_clusters(clusters_to_print, labels=None, n=0):
    """
    Print Clusters tree recursively
    :param clusters_to_print:
    :param labels:
    :param n:
    :return:
    """

    # indent to make hierarchy layout
    for i in range(n):
        print '  '
    if clusters_to_print.id < 0:
        # negative ids mean that this is branch
        print '-'
    else:
        # positive ids means that this is Endpoint
        if labels is None:
            print clusters_to_print.id
        else:
            print labels[clusters_to_print.id]
    # Now Print the Right and Left Branches
    if clusters_to_print.left is not None:
        print_clusters(clusters_to_print.left, labels=labels, n=n + 1)
    if clusters_to_print.right is not None:
        print_clusters(clusters_to_print.right, labels=labels, n=n + 1)


def rotate_matrix(data):
    rotated_matrix = []
    for i in range(len(data[0])):
        new_row = [data[j][i] for j in range(len(data))]
        rotated_matrix.append(new_row)
    return rotated_matrix


if __name__ == '__main__':
    print 'A. Hierarchical Clustering'
    print '1. Fetch data and create Hierarchical Clusters.'
    blog_names, words, data = read_file('../blogdata.txt')
    clusters = hierarchical_cluster(data)
    print_clusters(clusters, labels=blog_names)
    draw_dendogram(clusters, labels=blog_names, jpeg='blog_cluster.jpg')

    print '2. Lets rotate Matrix and do Column Clustering.'
    columnar_data = rotate_matrix(data)
    columnar_clusters = hierarchical_cluster(columnar_data)
    draw_dendogram(columnar_clusters, labels=words, jpeg='word_cluster.jpg')
    print ('3. K-Means Clustering')

    print ('End of Unsupervised Algorithms')