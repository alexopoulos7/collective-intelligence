from math import sqrt

from PIL import Image
from PIL import ImageDraw

from utilities import pearson_distance
from random import random


def scale_down(data, distance=pearson_distance, rate=0.01):
    """
    Take the data vector and return an array with 2 columns for the X,Y coordinates of the items on the
    two-dimensional chart.
    The distance between data points is calculated using by default pearson distance
    Algorithm:
    For every pair of items, the target distance is compared to the current distance and an error_term is calculated.
    Every item is moved a small amount closer or further in proportion to the error between the 2 items.
    Every node is moved according to the combination of all other nodes pushing and pulling on it.
    Each time this happens, the difference between the current distances and the target distances gets a bit smaller.
    This procedure is repeated many times until the total amount of error cannot be reduced any more.
    :param data: Input data
    :param distance: Distance function, Default: Pearson distance
    :param rate:
    :return:
    """
    n = len(data)

    # The real dimensions between every pair of items
    # here we convert data to 2D data
    read_list = [[distance(data[i], data[j]) for j in range(n)] for i in range(0, n)]

    # now we need to scale 2D data to show in image
    outersum = 0.0

    # Randomly initialize the starting points of the locations in 2D
    locations = [[random(), random()] for i in range(n)]
    fake_distance = [[0.0 for j in range(n)] for i in range(n)]

    last_error = None
    for m in range(0, 1000):
        # Find projected distances
        for i in range(n):
            for j in range(n):
                fake_distance[i][j] = sqrt(
                    sum([pow(locations[i][x] - locations[j][x], 2) for x in range(len(locations[i]))]))
        # Move points
        gradient = [[0.0, 0.0] for i in range(n)]

        total_error = 0
        for k in range(n):
            for j in range(n):
                if j == k:
                    continue
                # The error is percent difference between the distances
                error_term = (fake_distance[j][k] - read_list[j][k]) / read_list[j][k]

                # Each point needs to be moved away from or towards the other
                # point in proportion to how much error it has
                gradient[k][0] += ((locations[k][0] - locations[j][0]) / fake_distance[j][k]) * error_term
                gradient[k][1] += ((locations[k][1] - locations[j][1]) / fake_distance[j][k]) * error_term

                # Keep track of the total error
                total_error += abs(error_term)
        print 'Total Error: {}'.format(total_error)

        # if the answer got worse by moving the points, we are done
        if last_error and last_error < total_error:
            break
        last_error = total_error

        # Move each of the points by the learning rate times the gradient
        for k in range(n):
            locations[k][0] -= rate * gradient[k][0]
            locations[k][1] -= rate * gradient[k][1]

    return locations


def draw2d(data, labels, image_name='mds2d.jpg'):
    """
    Plot in 2 dimensional space the data and save as jpeg image
    :param data: 2 column array with X,Y coordinates
    :param labels: Names of nodes
    :param image_name: 'mds2d.jpg' as default
    :return: None, save image file
    """
    img = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    for i in range(len(data)):
        x = (data[i][0] + 0.5) * 1000
        y = (data[i][1] + 0.5) * 1000

        draw.text((x, y), labels[i], (0, 0, 0))
        # (x1,y1) = draw.textsize(labels[i])
        draw.point((x, y), fill=(255, 0, 0))
        # draw.polygon([(x,y),(x1,y),(x1,y1),(x,y1)],fill=(255,0,0))
        # draw.line((x,y, fill=(0,0,255),width=2)
    img.save(image_name, 'JPEG')
