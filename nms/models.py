from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from po.models import Po, Branch


class Isp(models.Model):
    name = models.CharField(max_length=100)

class nwData(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    isp = models.ForeignKey(Isp, on_delete=models.CASCADE)
    data = models.CharField(max_length=50)
    speed = models.CharField(max_length=50)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    last_recharge = models.DateField()

