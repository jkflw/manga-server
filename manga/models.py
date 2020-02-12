from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Directory(models.Model):
    """Holds directories with non dir files in them"""
    directory = models.TextField()
    full_path = models.TextField(unique = True)
    title = models.TextField(db_index = True)
    year = models.TextField(db_index = True)
    authors = ArrayField(models.TextField(), blank = True, db_index = True)
    genres = ArrayField(models.TextField(), blank = True, db_index = True)
    tags = ArrayField(models.TextField(), blank = True, db_index = True)
    related_series = ArrayField(models.TextField(), blank = True, db_index = True)
    completely_scanlated = models.BooleanField(default = False)
    manga_updates_link = models.TextField(db_index = True)
    manga_image = models.TextField()

class WatchedSeries(models.Model):
    series = models.ForeignKey(
        Directory,
        on_delete = models.CASCADE,
        db_index = True
    )
    #current_chapter_path = models.TextField()
    #current_page = models.IntegerField()

class Settings(models.Model):
    default_page_size = models.IntegerField()

