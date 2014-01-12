from django.conf.urls import patterns, include, url

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'cinema.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^employee/', include('employee_app.urls')),
    url(r'^client/', include('client.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
