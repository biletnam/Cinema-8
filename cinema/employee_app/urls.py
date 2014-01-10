from django.conf.urls import patterns, url

from employee_app import views

urlpatterns = patterns('',
    url(r'^login/$', views.login_page, name='login_page'),
    url(r'^logout/$', views.logout_page, name='logout_page'),

    url(r'^$', views.index, name='index'),
    url(r'^index/$', views.index, name='index'),
    url(r'^movies/$', views.movies, name='movies'),
        url(r'^movies/(?P<movie_id>\d+)/$', views.edit_movie, name='edit_movie'),
        url(r'^movies/add/$', views.add_movie, name='add_movie'),
    url(r'^rooms/$', views.rooms, name='rooms'),
        url(r'^rooms/(?P<room_id>\d+)/$', views.edit_room, name='edit_room'),
        url(r'^rooms/add/$', views.add_room, name='add_room'),
    url(r'^reservations/$', views.reservations, name='reservations'),
        url(r'^reservations/(?P<id>\d+)/$', views.view_reservation, name='view_reservation'),

)