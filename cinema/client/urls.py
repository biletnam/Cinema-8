from django.conf.urls import patterns, url


from client import views

urlpatterns = patterns('',

    url(r'^$', views.movies_view, name='movies_view'),
    url(r'^movies/(?P<movie_id>\d+)/$', views.projections_view, name='projections_view'), 
    url(r'^projection/(?P<proj_id>\d+)/$', views.seats_view, name='seats_view'),

)