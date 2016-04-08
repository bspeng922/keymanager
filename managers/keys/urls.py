# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

urlpatterns = patterns('managers.keys.views',
    url(r'^$', 'index', name='index'),
    url(r'^generate_keys$', 'generate_keys', name='generate_keys'),
    url(r'^(?P<key_id>.+)/reuse', 'reuse', name='reuse'),
    url(r'^(?P<key_id>.+)/edit', 'edit_version', name='edit_version'),
    url(r'^(?P<key_id>.+)/download', 'download_key_file', name='download'),
    url(r'^(?P<key_id>.+)/delete', 'delete', name='delete')
)
