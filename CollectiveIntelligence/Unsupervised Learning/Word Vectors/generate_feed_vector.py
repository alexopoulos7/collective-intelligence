import feedparser
import re

"""
Lets create a word count file from blog RSS feeds
We can use it afterwards to do some clustering experiments
"""


def get_word_counts(url):
    """
    Returns title and dictionary of word counts for an RSS Feed
    :param url: Url to parse feed
    :return: Returns title and dictionary of word counts for an RSS Feed
    """
    # parse the feed
    d = feedparser.parse(url)

    wc = {}

    # Loop over all entries
    for e in d.entries:
        if 'summary' in e:
            summary = e.summary
        else:
            summary = e.description

        # Extract a list of words
        words = get_words(e.title + ' ' + summary)
        for word in words:
            wc.setdefault(word, 0)
            wc[word] += 1
    if 'title' in d.feed:
        return d.feed.title, wc
    else:
        return None, {}  # url, wc


def get_words(blog):
    """
    Parse blog entry and return all words in lowercase
    :param blog: an html string
    :return: all words in lowercase
    """
    # remove all the html tags
    txt = re.compile(r'<[^>]+>').sub('', blog)

    # split words by all non-alpha characters
    words = re.compile(r'[^A-Z^a-z]+').split(txt)

    # convert to lowercase
    return [word.lower() for word in words if word != '']


def filter_word_list(blog_word_count, length_of_feed_list):
    """
    Filter word count. We do not want to include words like 'the', 'a', etc
    Here we include words with frequency > 10% and lower 50%
    :param length_of_feed_list:
    :param blog_word_count:
    :return: a word list that should be included
    """
    word_list = []
    upper_limit = 0.5
    lower_limit = 0.1
    for w, bc in blog_word_count.iteritems():
        fraction = float(bc) / length_of_feed_list
        if lower_limit < fraction < upper_limit:
            word_list.append(w)
    return word_list


def save_word_list(word_list, word_counts):
    """
    Save in text file a big matrix of all the words count for each blog
    tab delimeted
    :param word_list:
    :param word_counts:
    :return:
    """
    out = file('blogdata.txt', 'w')
    out.write('Blog')
    for word in word_list:
        out.write('\t%s' % word)
    out.write('\n')
    for blog, wc in word_counts.items():
        if blog is not None and len(blog) > 0:
            # deal with unicode outside ascii range
            blog = blog.encode('ascii', 'ignore')
            print 'Blog name is {}'.format(blog)
            out.write(blog)
            for word in word_list:
                if word in wc:
                    out.write('\t%d' % wc[word])
                else:
                    out.write('\t0')
            out.write('\n')


def generate():
    """
    Main function to generate the txt file with word counts
    :return: None
    """
    blog_count = {}
    feed_list = []
    word_counts = {}

    for feed_url in file('feedlist.txt'):
        feed_list.append(feed_url)
        title, wc = get_word_counts(feed_url)
        word_counts[title] = wc
        for word, count in wc.items():
            blog_count.setdefault(word, 0)
            if count > 1:
                blog_count[word] += 1

    # get word list
    word_list = filter_word_list(blog_count, len(feed_list))
    save_word_list(word_list, word_counts)


if __name__ == '__main__':
    generate()
