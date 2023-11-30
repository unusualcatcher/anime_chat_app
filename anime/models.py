from django.db import models

class Anime(models.Model):
    title = models.CharField(max_length=400)
    description = models.TextField(null=True)

    def __str__(self):
        return self.title