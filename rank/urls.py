from django.conf.urls import url

from rank.views import rank, rank_data

urlpatterns = [
    url(r'^$', rank,
        name='rank'),
    url(r'^data/$', rank_data,
        name='rank'),
]
