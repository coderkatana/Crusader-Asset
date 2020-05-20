from django.contrib import admin
from .models import Po, PoItem, Designations, Vendor, Employee, Departments, Branch


# class PoDetailsAdmin(admin.ModelAdmin):
#     list_display = ('po_number', 'created_at')


class PoAdmin(admin.ModelAdmin):
    list_display = ('po_number', 'total_cost')


admin.site.register(Po, PoAdmin)


class PoItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'quantity')


admin.site.register(PoItem, PoItemAdmin)


class BranchAdmin(admin.ModelAdmin):
    list_display = ('Name', 'phone')


admin.site.register(Branch, BranchAdmin)


class DesignationsAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Designations, DesignationsAdmin)


class DepartmentsAdmin(admin.ModelAdmin):
    list_display = ['title']


admin.site.register(Departments, DepartmentsAdmin)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation')


admin.site.register(Employee, EmployeeAdmin)


class VendorAdmin(admin.ModelAdmin):
    list_display = ('Name', 'phone')


admin.site.register(Vendor, VendorAdmin)
