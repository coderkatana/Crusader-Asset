from django import forms
from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from django.utils import timezone

# Create your models here.
from django.utils.timezone import now

from po.models import Po, Branch


class Status(models.Model):
    title = models.CharField(max_length=50)


class Assets(models.Model):
    STATUS_CHOICES = ("ACTIVE", "SCRAPPED", "FIXING")

    product_name = models.CharField(max_length=55)
    procurement_date = models.DateField('date created', default=timezone.now)
    warranty_expiration = models.DateField('warranty expiration', null=True)
    product_type = models.CharField(max_length=55)
    # product_user = models.CharField(max_length=55)
    po = models.ForeignKey(Po, on_delete=models.CASCADE, null=True)
    invoice_number = models.IntegerField()
    vendor_name = models.CharField(max_length=55)
    status = models.CharField(max_length=55, default="Active")

    notes = models.CharField(max_length=100)
    serial_no = models.CharField(max_length=100)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    print(warranty_expiration)

    def warranty_status(self, *args):
        date = datetime.date(datetime.now())
        if date > self.warranty_expiration:
            print('true')
            return 'Warranty expired'
        else:
            return 'In Warranty'


class AssetHistory(models.Model):
    old_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='old_branch')
    old_status = models.CharField(max_length=50)
    old_notes = models.CharField(max_length=200)
    new_branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name= 'new_branch')
    new_status = models.CharField(max_length=50)
    new_notes = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    asset = models.ForeignKey(Assets, on_delete=models.CASCADE)
    modified_at = models.DateTimeField(default=now, blank=True)

    def changePhrase(self):
        formatedDate = self.modified_at.strftime("%Y-%m-%d")
        formatedTime = self.modified_at.strftime("%H:%M")

        phrase = []
        if self.old_branch_id != self.asset.branch_id:
            branch_change = f"{formatedDate} : {self.user} changed asset branch from {self.old_branch.Name} to {self.new_branch.Name} at {formatedTime}."
            phrase.append(branch_change)

        if self.old_status != self.new_status:
            status_change = f"{formatedDate} : {self.user} changed asset status from {self.old_status} to {self.new_status} at {formatedTime}."
            phrase.append(status_change)

        if self.old_notes != self.new_notes:
            notes_change = f"{formatedDate} : {self.user} changed asset notes from {self.old_notes} to {self.new_notes} at {formatedTime}."
            phrase.append(notes_change)

        return phrase


class UrAssets(models.Model):
    product_name = models.CharField(max_length=100)
    procurement_date = models.DateField('date created', default=datetime.now, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=55, null=True)
    po = models.ForeignKey(Po, on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=55)
