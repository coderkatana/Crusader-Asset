from datetime import datetime
from django.db import models


# Create your models here.


class Make(models.Model):
    company = models.CharField(max_length=60)

    # auto_now_add=True
    def __str__(self):
        return self.company

class Type(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Product(models.Model):
    model_name = models.CharField(max_length=60)
    make = models.ForeignKey('Make', on_delete=models.CASCADE)
    desc = models.TextField()
    when = models.DateTimeField('date created', default=datetime.now)
    product_type = models.ForeignKey('Type', on_delete=models.CASCADE)

    def title(self):
        return self.make.company + " " + self.model_name

    def __str__(self):
        return self.title()
