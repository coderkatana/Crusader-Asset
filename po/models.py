from datetime import datetime
from django.apps import apps
from django.contrib.auth.models import User
from django.db import models
from products.models import Product, Make


class Departments(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Designations(models.Model):
    title = models.CharField(max_length=100)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.ForeignKey(Designations, on_delete=models.CASCADE)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Branch(models.Model):
    Name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.EmailField()
    # address
    door_no = street_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    road_address = models.CharField(max_length=100)

    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


class Vendor(models.Model):
    Name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    email = models.EmailField()
    # address
    door_no = street_address = models.CharField(max_length=100)
    street_address = models.CharField(max_length=100)
    road_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)

    def __str__(self):
        return self.Name


# def get_product_price(*args):
#     products = Product.objects.filter(id='id')
#     unit_price = products.price
#     return unit_price


class PoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"


def increment_po_number():
    last_po = Po.objects.all().order_by('id').last()
    if not last_po:
        return 'DNCIT2020-001'
    po_number = last_po.po_number
    po_int = int(po_number.split('DNCIT2020-')[-1])
    new_po_int = po_int + 1

    new_po_number = 'DNCIT2020-' + str('{0:03}'.format(new_po_int))
    return new_po_number


class Po(models.Model):
    po_item = models.ManyToManyField(PoItem)
    passer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='passer')
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='approved_by')
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    po_number = models.CharField(max_length=25, default=increment_po_number)
    processed_date = models.DateTimeField(auto_now_add=True, blank=True)

    def total_cost(self):
        po_items = self.po_item.all()
        cost = 0
        for po_item in po_items:
            cost += po_item.get_total_price()
        return cost


    def __int__(self, po_number):
        return self.po_number()
