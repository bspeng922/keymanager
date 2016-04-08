from django.db import models


class Version(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    key = models.CharField(max_length=2)
    name = models.CharField(max_length=20)
    vmemory_limit = models.FloatField()
    server_limit = models.FloatField()
    deleted = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'version'
