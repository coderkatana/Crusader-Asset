from django import forms
from django.forms import ModelForm

from po.models import Branch
from .models import Assets


# class AssetForm(forms.ModelForm):
#     class Meta:
#         model = Assets
#         template_name = 'add_assets.html'
#         fields = [
#             'product_name',
#             'procurement_date',
#             'warranty_expiration',
#             'branch_assigned',
#             'product_type',
#             # 'life_expectancy',
#             # product_user
#             # 'po_number',
#             'invoice_number',
#             'vendor_name',
#             'notes'
#         ]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['branch_assigned'].queryset = Branch.objects.all()
