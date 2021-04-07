from django.db import models

# Create your models here.
class Stock(models.Model):
    code = models.PositiveIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    open = models.FloatField(default=0, blank=True)
    high = models.FloatField(default=0, blank=True)
    low = models.FloatField(default=0, blank=True)
    close = models.FloatField(default=0, blank=True)

    def __str__(self):
        return str(self.name)
