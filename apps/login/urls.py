from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^process_register$', views.process),
    url(r'^authenticate$', views.authenticate),
    url(r'^logout$', views.logout),
    url(r'^post_secret$', views.post_secret),
    url(r'^like/(?P<secret_id>\d+)$', views.like_secret),
    url(r'^unlike/(?P<secret_id>\d+)$', views.unlike_secret),
    url(r'^secret/delete/(?P<secret_id>\d+)$', views.delete_secret)
]
