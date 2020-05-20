from import_export import resources
from .models import Po


class PoExport(resources.ModelResource):
    class Meta:
        model = Po
