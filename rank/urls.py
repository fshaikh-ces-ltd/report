from django.conf.urls import url

from rank.views import quotation

urlpatterns = [
    url(r'^rank/$', quotation,
        name='quotation'),
]
