from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^beach/(?P<beach_name>.+)$', views.show_beach, name='show_beach'),
]
