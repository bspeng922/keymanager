# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

from managers.versions.models import Version


class ActivationKey(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    key = models.CharField(max_length=48)
    # version = models.ForeignKey(Version)
    version = models.CharField(max_length=50)
    srv_limit = models.IntegerField(default=1)
    cpu_limit = models.IntegerField(default=1)
    company = models.CharField(max_length=200, default="N/A")
    machine_code = models.CharField(max_length=64, null=True)
    user = models.ForeignKey(User)
    used = models.IntegerField(default=0)
    deleted = models.IntegerField(default=0)
    activation_time = models.DateTimeField(null=True)
    generation_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.key

    class Meta:
        ordering = ['-generation_time']
        db_table = 'activation_key'
