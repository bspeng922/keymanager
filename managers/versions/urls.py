from django.conf.urls import patterns, url

urlpatterns = patterns('managers.versions.views',
    url(r'^$', 'index', name='index'),
    url(r'^create$', 'create', name='create'),
    url(r'^(?P<version_id>.+)/delete$', 'delete', name='delete')
)
