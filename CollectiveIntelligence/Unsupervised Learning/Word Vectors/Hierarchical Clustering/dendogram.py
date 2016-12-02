from PIL import Image, ImageDraw


def get_height(cluster):
    """
    Get total Height of a given Cluster
    :param cluster: BiCluster
    :return: integer
    """
    # if this is an endpoint then height is just 1
    if cluster.left is None and cluster.right is None:
        return 1
    # otherwise lets calculate recursively the height of each branch
    return get_height(cluster.left) + get_height(cluster.right)


def get_depth(cluster):
    """
    This is the total error of the root node
    Since the length of the lines will be scaled to how much error is in each row, we ll be generating a scaling factor
    based on how much total error there is
    :param cluster:
    :return:
    """
    if cluster.left is None and cluster.right is None:
        return 0
    # the distance of a branch is the max of the 2 branches plus its own distance
    return max(get_depth(cluster.left), get_depth(cluster.right)) + cluster.distance


def draw_dendogram(cluster, labels, jpeg='clusters.jpg', w=1200):
    """
    Initialize, Draw and Save Image with cluster dendogram
    :param cluster:
    :param labels:
    :param jpeg:
    :param w:
    :return:
    """
    # height and width
    h = get_height(cluster) * 20
    depth = get_depth(cluster)

    # As width is fixed lets scale distances accordingly
    scaling = float(w - 150) / depth

    # create new image with white background
    img = Image.new('RGB', (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    draw.line((0, h / 2, 10, h / 2), fill=(255, 0, 0))

    # Draw the first node
    draw_node(draw, cluster, 10, (h / 2), scaling, labels)
    img.save(jpeg, 'JPEG')


def draw_node(draw, cluster, x, y, scaling, labels):
    """

    :param draw:
    :param cluster:
    :param x:
    :param y:
    :param scaling:
    :param labels:
    :return:
    """
    if cluster.id < 0:
        height_left = get_height(cluster.left) * 20
        height_right = get_height(cluster.right) * 20

        top = y - (height_left + height_right) / 2
        bottom = y + (height_left + height_right) / 2

        line_length = cluster.distance * scaling

        # Vertical line from this cluster to children
        draw.line((x, top + height_left / 2, x, bottom - height_right / 2), fill=(255, 0, 0))

        # Horizontal line to left item
        draw.line((x, top + height_left / 2, x + line_length, top + height_left / 2), fill=(255, 0, 0))

        # Horizontal line to right item
        draw.line((x, bottom - height_right / 2, x + line_length, bottom - height_right / 2), fill=(255, 0, 0))

        # Recursively draw left and right branches
        if cluster.left is not None:
            draw_node(draw, cluster.left, x + line_length, top + height_left / 2, scaling, labels)
        if cluster.right is not None:
            draw_node(draw, cluster.right, x + line_length, bottom - height_right / 2, scaling, labels)
    else:
        # if this is the endpoint
        draw.text((x + 5, y - 7), labels[cluster.id], (0, 0, 0))
