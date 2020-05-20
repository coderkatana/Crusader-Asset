from django.contrib import admin

# Register your models here.
from nms.models import Isp


class IspAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Isp, IspAdmin)