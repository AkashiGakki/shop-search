from django.db import models


class User(models.Model):
    id = models.AutoField(max_length=12, primary_key=True)
    name = models.CharField(max_length=20)
    age = models.IntegerField(null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    password = models.CharField(max_length=16)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=30)

    def __str__(self):
        return self.name
