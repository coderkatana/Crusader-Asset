from django.contrib import admin
from .models import Product, Make, Type


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Product, ProductAdmin)


class MakeAdmin(admin.ModelAdmin):
    list_display = ('company',)


admin.site.register(Make, MakeAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('title',)


admin.site.register(Type, TypeAdmin)
