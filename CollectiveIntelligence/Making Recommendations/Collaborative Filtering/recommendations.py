from data_storage import critics
from math import sqrt
import pprint


###
# USER BASED COLLABORATION FILTER
###


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


def sim_tanimoto(preferences, person1, person2):
    """
    Compute the difference between person1 and person2 preferences using Tanimoto formula
    http://mines.humanoriented.com/classes/2010/fall/csci568/portfolio_exports/sphilip/tani.html
    :param preferences: the dictionary of preferences. The key is the name of persons
    :param person1: Name of first person
    :param person2: Name of second person
    :return: [0,1] distance score, 1 means identical preferences
    :return:
    """
    common_movies = [item for item in preferences[person1] if item in preferences[person2]]
    length_of_common_movies = len(common_movies)
    if length_of_common_movies == 0:
        return 0
    don = len(preferences[person1]) + len(preferences[person2]) - length_of_common_movies

    return length_of_common_movies / float(don)


def sim_tanimoto_sets(preferences, person1, person2):
    person1_set = set(preferences[person1])
    person2_set = set(preferences[person2])
    print '{} preferences as a set {}'.format(person1, person1_set)

    length_of_common_movies = len(set.intersection(*[person1_set, person2_set]))

    union_cardinality = len(set.union(*[person1_set, person2_set]))
    if length_of_common_movies == 0:
        return 0

    return length_of_common_movies / float(union_cardinality)


def square_rooted(x):
    return round(sqrt(sum([a*a for a in x])), 3)


def sim_cosine(preferences, person1, person2):
    si = {}
    # common preferences
    for item in preferences[person1]:
        if item in preferences[person2]:
            si[item] = 1

    # if they have no common preferences return 0
    if len(si) == 0:
        return 0

    # Calculate cosine similarity using common preferences
    x = [preferences[person1][item] for item in si]
    y = [preferences[person2][item] for item in si]

    # Calculate cosine similarity using all preferences
    # x = preferences[person1].values()
    # y = preferences[person2].values()
    print x, y
    numerator = sum(a * b for a, b in zip(x, y))
    denominator = square_rooted(x) * square_rooted(y)
    return round(numerator / float(denominator), 3)


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
    :param preferences: the dictionary of preferences. The key is the name of persons
    :return: Dictionary of flipped items with users
    """
    result = {}
    for person in preferences:
        for item in preferences[person]:
            result.setdefault(item, {})

            # Flip item and person
            result[item][person] = preferences[person][item]
    return result


###
# Item Based Collaboration Filtering
###
def calculate_similar_items(preferences, n=10, similarity=sim_pearson):
    """
    Calculate and return a dictionary with Items scores
    :param preferences: the dictionary of preferences. The key is the item
    :param n: how many items
    :param similarity: which similarity function should create
    :return:
    """
    # create a dictionary of items showing which other items they are most similar to
    result = {}

    item_preferences = transform_preferences(preferences)
    c = 0
    for item in item_preferences:
        # status updates for large datasets
        c += 1
        if c % 100 == 0:
            print "%d / %d" % (c, len(item_preferences))
        # find the most similar items to this one
        scores = top_matches(item_preferences, item, n=n, similarity=similarity)
        result[item] = scores
    return result


def get_recommended_items(preferences, item_match, user):
    """
    Return a list of recommended items
    :param preferences:the dictionary of preferences. The key is the name of the user
    :param item_match: the result of  calculate_similar_items
    :param user: user name
    :return: a list
    """
    # get ratings of items from user
    user_ratings = preferences[user]
    scores = {}
    total_sim = {}

    # Loop over items rated by this user
    for (item, rating) in user_ratings.items():
        # Loop over items similar to this one
        for (similarity, item2) in item_match[item]:
            # Ignore item if user has already rate this item
            if item2 in user_ratings:
                continue

            # weighted sum of rating times similarity
            scores.setdefault(item2, 0)
            scores[item2] += similarity * rating

            # Sum all the similarities
            total_sim.setdefault(item2, 0)
            total_sim[item2] += similarity

    # Divide each total score by total weighting to get an average
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    # Return the rankings from highest to lowest
    rankings.sort()
    rankings.reverse()
    return rankings


# Main Method to compare distances
if __name__ == '__main__':
    pers1 = 'Lisa Rose'
    pers2 = 'Michael Philips'
    movie1 = 'Superman Returns'
    movie2 = 'Just My Luck'
    num_of_matches = 3

    # Calculate Euclidean
    ed = sim_distance(critics, pers1, pers2)
    print 'Euclidean Distance Score between {} and {} is {}'.format(pers1, pers2, ed)

    # Calculate Pearson
    pr = sim_pearson(critics, pers1, pers2)
    print 'Pearson Correlation Coefficient Score between {} and {} is {}'.format(pers1, pers2, pr)

    # Calculate Tanimoto
    tan = sim_tanimoto(critics, pers1, pers2)
    print 'Tanimoto Correlation Coefficient Score between {} and {} is {}'.format(pers1, pers2, tan)

    # Calculate Cosine
    tan_sets = sim_cosine(critics, pers1, pers2)
    print 'Cosine Similarity Score between {} and {} is {}'.format(pers1, pers2, tan_sets)

    # Get top 3 matches for Lisa
    top_3_matches = top_matches(critics, pers1, num_of_matches)
    print 'Top 3 matches for {} are {} using Pearson'.format(pers1, top_3_matches)

    # Get top 3 matches for Lisa using Euclidean
    top_3_matches = top_matches(critics, pers1, num_of_matches, sim_distance)
    print 'Top 3 matches for {} are {} using Euclidean'.format(pers1, top_3_matches)

    # Get Recommendations
    recommendations = get_recommendations(critics, 'Toby')
    print 'Recommended movies for {} are {} using Pearson'.format('Toby', recommendations)

    # Get Recommendations using Euclidean
    recommendations = get_recommendations(critics, 'Toby', sim_distance)
    print 'Recommended movies for {} are {} using Euclidean'.format('Toby', recommendations)

    movies = transform_preferences(critics)
    # Get top 3 matches for Movie Superman Returns
    top_3_matches_movies = top_matches(movies, movie1, num_of_matches, sim_pearson)
    print 'Top 3 movie matches for {} are {} using Pearson '.format(movie1, top_3_matches_movies)

    # Get top 3 matches for Movie Superman Returns using Euclidean
    top_3_matches_movies = top_matches(movies, movie1, num_of_matches, sim_distance)
    print 'Top 3 movie matches for {} are {} using Pearson '.format(movie1, top_3_matches_movies)

    # Get recommendations for specified movie
    print 'Get Recommendations if I have seen movie {}, {}'.format(movies, get_recommendations(movies, movie2))
    pp = pprint.PrettyPrinter(indent=4)
    items_dictionary = calculate_similar_items(critics, 10, sim_distance)

    # Item-based Collaboration Filtering
    pp.pprint('Show all Similar Items {}'.format(items_dictionary))

    print('Recommended items are {} for {} '.format(get_recommended_items(critics, items_dictionary, 'Toby'), 'Toby'))
