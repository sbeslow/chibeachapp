from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^beach/(?P<beach_name>.+)$', views.show_beach, name='show_beach'),
    url(r'^chicago$', views.chicago, name='is_your_beach_safe'),
]
