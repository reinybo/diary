from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse


class Entry(models.Model):
    title = models.CharField(max_length = 250)
    date = models.DateField()
    content = models.TextField(max_length = 10000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse('detail', kwargs={'entry_id': self.id})


class Photo(models.Model):
    url = models.CharField(max_length=200)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for entry_id: {self.entry_id} @{self.url}"