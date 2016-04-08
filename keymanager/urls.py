from django.conf.urls import patterns, include, url

from managers.users.views import login, logout
from managers.keys.views import key_available, use_key, deactivate


urlpatterns = patterns('',
    url(r'^$', login, name='index'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^key_available/', key_available, name='key_available'),
    url(r'^use_key/', use_key, name='use_key'),
    url(r'^deactivate/', deactivate, name='deactivate'),
    url(r'^keys/', include('managers.keys.urls', namespace='keys')),
    url(r'^users/', include('managers.users.urls', namespace='users')),
    url(r'^versions/', include('managers.versions.urls', namespace='versions'))
)
