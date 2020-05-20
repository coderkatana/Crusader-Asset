from django.contrib import admin
from .models import Assets


# Register your models here.
class AssetsAdmin(admin.ModelAdmin):
    list_display = ('invoice_number',)


admin.site.register(Assets, AssetsAdmin)
