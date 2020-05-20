from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from products.models import Product
from .filters import PoFilter
from .models import Po, PoItem
from assets.models import UrAssets
from datetime import datetime


class IndexView(ListView):
    model = Po
    template_name = 'poList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PoFilter(self.request.GET, queryset=self.get_queryset().order_by('processed'))
        # print(PoFilter(self.request.GET, queryset=self.get_queryset().order_by('processed')).qs)
        total = 0
        for po in context['filter'].qs:
            total+=po.total_cost()
        context['total'] = total
        return context


class CreateView(CreateView):
    model = Po
    template_name = 'createPo.html'


class DetailView(DetailView):
    model = Po
    template_name = 'po_template.html'


class DeleteView(generic.DeleteView):
    model = Po
    template_name = 'poList.html'


def process_po(request, po_id):
    po = get_object_or_404(Po, pk=po_id)
    po_item = PoItem.objects.all().filter(po=po_id)

    for items in po_item:
        product = get_object_or_404(Product, id=items.product_id)
        while items.quantity > 0:
            product_title = str(product.make) + '-' + str(product.model_name)
            print(product_title)
            ura = UrAssets(po_id=po.id, vendor_name=po.vendor, product_name=product_title,
                           product_type=product.product_type, branch_id=po.branch.id)
            ura.save()
            items.quantity -= 1

    print(po.__dict__)

    po.processed = True
    po.processed_date = datetime.now()
    po.save()

    return HttpResponseRedirect(reverse('po:index'))
