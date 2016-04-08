# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns("managers.users.views",
    url(r'^$', 'index', name='index'),
    url(r'^create$', 'create', name='create'),
    url(r'^(?P<user_id>.+)/delete', 'delete', name='delete'),
    url(r'^(?P<user_id>.+)/activate', 'activate', name='activate'),
    url(r'^(?P<user_id>.+)/deactivate', 'deactivate', name='deactivate'),
    url(r'^(?P<user_id>.+)/edit', 'edit', name='edit')
)
