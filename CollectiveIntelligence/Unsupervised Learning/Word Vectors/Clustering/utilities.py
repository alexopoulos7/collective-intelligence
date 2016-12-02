from math import sqrt


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
