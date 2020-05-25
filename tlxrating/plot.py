import os
import io
import time
from collections import namedtuple
import datetime as dt

from matplotlib import pyplot as plt


Rank = namedtuple('Rank', 'low high title title_abbr color_graph')
TLX_RANKS = (
    Rank(-10**9, 1650, 'Gray', 'N', '#b7b7b7'),
    Rank(1650, 1750, 'Green', 'P', '#70ad47'),
    Rank(1750, 2000, 'Blue', 'E', '#3c78d8'),
    Rank(2000, 2200, 'Purple', 'CM', '#7030a0'),
    Rank(2200, 2500, 'Yellow', 'IM', '#f6b26b'),
    Rank(2500, 3000, 'Red', 'IGM', '#FF0000'),
    Rank(3000, 10**9, 'Legend', 'LGM', '#AA0000')
)

# String wrapper to avoid the underscore behavior in legends
#
# In legends, matplotlib ignores labels that begin with _
# https://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
# However, this check is only done for actual string objects.
class StrWrap:
    def __init__(self, s):
        self.string = s
    def __str__(self):
        return self.string


def get_current_figure_as_file():
    filename = os.path.join(f'tempplot_{time.time()}.png')
    plt.savefig(filename, facecolor=plt.gca().get_facecolor(), bbox_inches='tight', pad_inches=0.25)

    with open(filename, 'rb') as file:
        content = io.BytesIO(file.read())

    os.remove(filename)
    return content


def plot_rating_bg(ranks):
    ymin, ymax = plt.gca().get_ylim()
    bgcolor = plt.gca().get_facecolor()
    for rank in ranks:
        plt.axhspan(rank.low, rank.high, facecolor=rank.color_graph, alpha=0.8, edgecolor=bgcolor, linewidth=0.5)

    locs, labels = plt.xticks()
    for loc in locs:
        plt.axvline(loc, color=bgcolor, linewidth=0.5)
    plt.ylim(ymin, ymax)


def plot_rating_changes(rating_changes):
    for user_rating_change in rating_changes:
        ratings, times = [], []
        for contest_history in user_rating_change:
            ratings.append(contest_history.rating)
            times.append(dt.datetime.fromtimestamp(contest_history.time // 1000))

        plt.plot(times,
                 ratings,
                 linestyle='-',
                 marker='o',
                 markersize=3,
                 markerfacecolor='white',
                 markeredgewidth=0.5)

    plt.gcf().autofmt_xdate()


def plot_tlx_rating(usernames, rating_changes):
    plt.switch_backend('Agg')
    plot_rating_changes(rating_changes)
    plot_rating_bg(TLX_RANKS)
    
    current_ratings = [rating_changes[-1].rating if rating_changes else 'Unrated' for rating_changes in rating_changes]
    labels = [f'{username} ({rating})' for username, rating in zip(usernames, current_ratings)]
    plt.legend(labels, loc='upper left')
