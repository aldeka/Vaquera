from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),
    
    (r'^$', mysite.vaquera.views.issue_index),
    (r'^issues/$', mysite.vaquera.views.issue_index),
    (r'^issues/(?P<issue_id>\d+)/$', mysite.vaquera.views.issue),
    (r'^issues/new/$', mysite.vaquera.views.new_issue),
    (r'^people/$', mysite.vaquera.views.people_index),
    (r'milestones/$', mysite.vaquera.views.milestone_index),
    (r'milestones/current/$', mysite.vaquera.views.current_milestone),
    (r'milestones/(?P<milestone_id>\d+)/$', mysite.vaquera.views.milestone),
    (r'(?P<username>.+)/issues_authored/$', mysite.vaquera.views.issues_authored),
    (r'(?P<username>.+)/issues_assigned/$', mysite.vaquera.views.issues_assigned),
    (r'(?P<username>.+)/issues_followed/$', mysite.vaquera.views.issues_followed),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
