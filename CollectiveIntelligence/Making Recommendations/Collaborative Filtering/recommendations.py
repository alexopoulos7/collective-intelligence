from data_storage import critics
from math import sqrt


def sim_distance(preferences, person1, person2):
    # type: (object, object, object) -> object
    """
    Calculate Euclidean Distance score between 2 persons
    :param preferences: the dictionary of preferences. The key is the name of persons
    :param person1: Name of first person
    :param person2: Name of second person
    :return: [0,1] distance score, 1 means identical preferences
    """
    # create empty dictionary of common preferences
    si = {}

    # common preferences
    for item in preferences[person1]:
        if item in preferences[person2]:
            si[item] = 1

    # if they have no common preferences return 0
    if len(si) == 0:
        return 0

    sum_of_squares = sum([pow(preferences[person1][item] - preferences[person2][item], 2) for item in si])

    return 1 / (1 + sqrt(sum_of_squares))


def sim_pearson(preferences, person1, person2):
    """
    Calculate Pearson Correlation Score
    The correlation coefficient is a measure of how well 2 sets of data fit on a straight line
    It corrects for grade inflation
    :param preferences: the dictionary of preferences. The key is the name of persons
    :param person1: Name of first person
    :param person2: Name of second person
    :return: [0,1] distance score, 1 means identical preferences
    """

    # lets find common preferences
    si = {}
    for item in preferences[person1]:
        if item in preferences[person2]:
            si[item] = 1

    n = len(si)

    if n == 0:
        return 0

    # Add all preferences for each person
    sum1 = sum([preferences[person1][item] for item in si])
    sum2 = sum([preferences[person2][item] for item in si])

    # Sum up the squares
    sum1_square = sum([pow(preferences[person1][item], 2) for item in si])
    sum2_square = sum([pow(preferences[person2][item], 2) for item in si])

    # Sum up the products
    product_sum = sum(preferences[person1][item] * preferences[person2][item] for item in si)

    # Calculate Pearson Score
    num = product_sum - (sum1 * sum2 / n)
    den = sqrt((sum1_square - pow(sum1, 2) / n) * (sum2_square - pow(sum2, 2) / n))
    if den == 0:
        return 0
    r = num / den

    return r


def top_matches(preferences, person, n=5, similarity=sim_pearson):
    """
    Returns the best matches for person from the preferences dictionary
    :param preferences: the dictionary of preferences. The key is the name of persons
    :param person:
    :param n:
    :param similarity: Which similarity function should be used
    :return:
    """
    scores = [(similarity(preferences, name, person), name) for name in preferences if name != person]

    # # Equivalent
    # for name in preferences:
    #     print name
    #     if name != person:
    #         sc = similarity(preferences, name, person)
    #         print ('Add sc {} for {}'.format(sc,name))
    #         scores.append((sc,name))
    scores.sort()
    scores.reverse()
    return scores[0:n]


def get_recommendations(preferences, person, similarity=sim_pearson):
    """
    Recommend movies for a person
    :param preferences: the dictionary of preferences. The key is the name of persons
    :param person:
    :param similarity:
    :return: list of movies
    """
    totals = {}
    sim_sums = {}
    for other in preferences:
        if other == person:
            continue
        sim = similarity(preferences, person, other)
        # Ignore scores of 0 or lower
        if sim <= 0:
            continue
        for item in preferences[other]:
            # only score movies person has not seen yet
            if item not in preferences[person] or preferences[person][item] == 0:

                # set default
                totals.setdefault(item, 0)
                # Add the product of similarity score times the rating
                totals[item] += preferences[other][item] * sim
                # Sum of similarities
                sim_sums.setdefault(item, 0)
                sim_sums[item] += sim

    # Normalize the sums
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

    rankings.sort()
    rankings.reverse()
    return rankings


def transform_preferences(preferences):
    """
    Transform a Dictionary of User Preferences to a dictionary of Products
    This way we can show related movies, etc
    :param preferences:
    :return:
    """
    result = {}
    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item,{})

            #Flip item and person
            result[item][person]=preferences[person][item]
    return result

# Main Method to compare distances
if __name__ == '__main__':
    pers1 = 'Lisa Rose'
    pers2 = 'Michael Philips'
    movie1 = 'Superman Returns'
    movie2 = 'Just My Luck'
    n = 3

    # Calculate Euclidean
    ed = sim_distance(critics, pers1, pers2)
    print 'Euclidean Distance Score between {} and {} is {}'.format(pers1, pers2, ed)

    # Calculate Pearson
    pr = sim_pearson(critics, pers1, pers2)
    print 'Pearson Correlation Coefficient Score between {} and {} is {}'.format(pers1, pers2, pr)


    # Get top 3 matches for Lisa
    top_3_matches = top_matches(critics, pers1, n)
    print 'Top 3 matches for {} are {} using Pearson'.format(pers1, top_3_matches)

    # Get top 3 matches for Lisa using Euclidean
    top_3_matches = top_matches(critics, pers1, n, sim_distance)
    print 'Top 3 matches for {} are {} using Euclidean'.format(pers1, top_3_matches)


    # Get Recommendations
    recommendations = get_recommendations(critics, 'Toby')
    print 'Recommended movies for {} are {} using Pearson'.format('Toby', recommendations)

    # Get Recommendations using Euclidean
    recommendations = get_recommendations(critics, 'Toby', sim_distance)
    print 'Recommended movies for {} are {} using Euclidean'.format('Toby', recommendations)


    movies = transform_preferences(critics)
    # Get top 3 matches for Movie Superman Returns
    top_3_matches_movies = top_matches(movies, movie1, 3, sim_pearson)
    print 'Top 3 movie matches for {} are {} using Pearson '.format(movie1,top_3_matches_movies)

    # Get top 3 matches for Movie Superman Returns using Euclidean
    top_3_matches_movies = top_matches(movies, movie1, 3, sim_distance)
    print 'Top 3 movie matches for {} are {} using Pearson '.format(movie1, top_3_matches_movies)

    # Get recommendations for specified movie
    print get_recommendations(movies, movie2)