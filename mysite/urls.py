from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    
    (r'^$', direct_to_template, mysite.vaquera.views.issue_index),
    (r'^issues/(?P<issue_id>\d+)/$', mysite.vaquera.views.issue),
    (r'^people/$', mysite.vaquera.views.people_index),
    (r'milestones/$', mysite.vaquera.view.milestone_index),
    (r'milestones/current/$', mysite.vaquera.view.current_milestone),
    (r'milestones/future/$', mysite.vaquera.view.future_milestones),
    (r'milestones/past/$', mysite.vaquera.view.past_milestones),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
