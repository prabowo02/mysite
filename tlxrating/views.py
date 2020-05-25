from django.http import HttpResponse
from django.shortcuts import render

from . import tlx, plot


TLX_RATING_RESPONSE = '''
<form action="/tlxrating" method="GET">
  <input name="usernames" placeholder="List of comma separated usernames" size="50"></input>
  <input type="submit" />
</form>
'''


def tlxrating(request):
    usernames = request.GET.get('usernames')
    if not usernames:
        return HttpResponse(TLX_RATING_RESPONSE)

    usernames = [username.strip() for username in usernames.split(',')]
    try:
        rating_changes = [tlx.rating(username=username) for username in usernames]
    except tlx.TlxApiError as e:
        return HttpResponse(TLX_RATING_RESPONSE + str(e))

    plot.plot_tlx_rating(usernames, rating_changes)
    return HttpResponse(plot.get_current_figure_as_file(), content_type='image/png')
