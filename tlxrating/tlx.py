from collections import namedtuple

import requests


API_BASE_URL = 'https://uriel.tlx.toki.id/api/v2/'
CONTEST_HISTORY_URL = 'contest-history/public/'

RatingChange = namedtuple('RatingChange', 'rating time')


class TlxApiError(Exception):
    def __init__(self, message=None):
        super().__init__(message or 'TLX API error')


def _query_api(path, params=None):
    message = None
    try:
        response = requests.get(API_BASE_URL + path, params=params)
        return response.json()
    except requests.Timeout:
        message = 'TLX API Timeout'
    except ValueError:
        message = 'TLX content error'

    raise TlxApiError(message)


def rating(*, username):
    params = {'username': username}
    response = _query_api(CONTEST_HISTORY_URL, params)
    if response.get('errorCode') == 'NOT_FOUND':
        raise TlxApiError('Username not found')

    try:
        data, contests_map = response['data'], response['contestsMap']
        return [RatingChange(contest_history['rating']['publicRating'], contests_map[contest_history['contestJid']]['beginTime'])
                for contest_history in data if contest_history['rating']]
    except:
        raise TlxApiError('TLX data error')
