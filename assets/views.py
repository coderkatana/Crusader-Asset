import csv

from po.models import Branch, Vendor
from products.models import Product, Type
from .filters import AssetsFilter, UrAssetsFilter
from .models import Assets, UrAssets, AssetHistory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

class IndexView(ListView):
    model = Assets
    template_name = 'assets_list.html'
    context_object_name = 'context'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AssetsFilter(self.request.GET, queryset=self.get_queryset())
        count = 0

        for asset in context['filter'].qs:
            count += 1
        context['result_count'] = count
        return context


# class AssetExportView(IndexView):
#     template_name = 'SavedSamples.csv'
#     content_type = 'text/csv'
# response = HttpResponse(content_type='text/csv')
# response['Content-Disposition'] = 'attachment;filename="users.csv"'
# writer = csv.writer(response)
# writer.writerow(
#     ['product_name', 'branch__Name', 'procurement_date', 'warranty_expiration', 'product_type', 'po__po_number',
#     'invoice_number',
#     'vendor_name', 'status', 'notes', 'serial_no'])
# assets = context['filter'].qs.values_list('product_name', 'branch__Name', 'procurement_date', 'warranty_expiration',
#                                     'product_type', 'po__po_number', 'invoice_number',
#                                     'vendor_name', 'status', 'notes', 'serial_no')
# for asset in assets:
#     writer.writerow(asset)
# return response

def asset_export(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(
        ['product_name', 'branch__Name', 'procurement_date', 'warranty_expiration', 'product_type', 'po__po_number',
         'invoice_number',
         'vendor_name', 'status', 'notes', 'serial_no'])
    assets = Assets.objects.all().values_list('product_name', 'branch__Name', 'procurement_date', 'warranty_expiration',
                                              'product_type', 'po__po_number', 'invoice_number',
                                              'vendor_name', 'status', 'notes', 'serial_no')
    for asset in assets:
        writer.writerow(asset)
    return response


def add_view(request):
    product_types = Type.objects.all().order_by('title')
    branches = Branch.objects.all().order_by('Name')
    vendors = Vendor.objects.all().order_by('Name')

    if request.method == 'POST':
        assets = Assets()
        assets.product_name = request.POST.get('product_name')
        assets.po_number = request.POST.get('po_number')
        assets.serial_no = request.POST.get('serial_no')
        assets.procurement_date = request.POST.get('procurement_date')
        assets.warranty_expiration = request.POST.get('warranty_expiration')
        assets.branch_id = request.POST.get('branch_dropdown')
        assets.product_type = request.POST.get('product_dropdown')
        assets.invoice_number = request.POST.get('invoice_number')
        assets.vendor_id = request.POST.get('vendor_dropdown')
        assets.notes = request.POST.get('notes')
        assets.po = request.POST.get('po_number')
        assets.save()
        return HttpResponseRedirect(reverse('assets:asset_detail_view', args=(assets.id,)))
    else:
        return render(request, 'add_assets.html',
                      {'branches': branches, 'product_types': product_types, 'vendors': vendors})


def ura_to_asset_view(request, ura_id):
    ura = get_object_or_404(UrAssets, pk=ura_id)
    branches = Branch.objects.all().order_by('Name')

    if request.method == 'POST':
        assets = Assets()
        assets.product_name = request.POST.get('product_name')
        assets.po_number = request.POST.get('po_number')
        assets.serial_no = request.POST.get('serial_no')
        assets.procurement_date = request.POST.get('procurement_date')
        assets.warranty_expiration = request.POST.get('warranty_expiration')
        assets.branch_id = ura.branch_id
        assets.product_type = request.POST.get('product_type')
        assets.invoice_number = request.POST.get('invoice_number')
        assets.vendor_name = request.POST.get('vendor_name')
        assets.notes = request.POST.get('notes')
        # assets.po_number = request.POST.get('po_number')
        assets.po_id = ura.po_id
        assets.save()

        ura.delete()
        return HttpResponseRedirect(reverse('assets:asset_detail_view', args=(assets.id,)))
    else:
        return render(request, 'add_assets.html', {'branches': branches, 'ura': ura})


# def add_view(request):
#     form = AssetForm(request.POST or None)
#     if form.is_valid():
#         form.save()
#         #form = AssetForm
#     context = {
#         'form': form
#     }
#     return render(request, 'add_assets.html', context)


class UrAView(ListView):
    model = UrAssets
    template_name = 'ur_assets_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = UrAssetsFilter(self.request.GET, queryset=self.get_queryset().order_by('-procurement_date'))
        count = 0
        for asset in context['filter'].qs:
            count += 1
        context['result_count'] = count
        return context


# class AssetDetailView(DetailView):
#     model = Assets
#     template_name = 'asset_detail_view.html'

def asset_detail_view(request, asset_id):
    asset = get_object_or_404(Assets, pk=asset_id)
    asset_histories = AssetHistory.objects.filter(asset_id=asset_id).order_by('-modified_at')
    return render(request, 'asset_detail_view.html', {'asset_histories': asset_histories, 'asset': asset})


# def asset_update_view(request, asset_id):
#     asset =get_object_or_404(Assets, pk=asset_id)
#     branch = Branch.objects.all()
#     print(asset.product_name)
#     return render(request, 'assets_form.html', {'asset':asset, 'branch':branch})

def asset_update_view(request, asset_id):
    asset = get_object_or_404(Assets, pk=asset_id)
    branches = Branch.objects.all().order_by('Name')
    asset_instance = AssetHistory()
    asset_instance.old_branch_id = asset.branch_id
    asset_instance.old_status = asset.status
    asset_instance.old_notes = asset.notes

    if request.method == 'POST':
        user = request.user
        print(user)
        asset.branch_id = request.POST.get('branch_dropdown')
        asset.status = request.POST.get('status').capitalize()
        asset.notes = request.POST.get('notes')
        asset.save()
        asset = get_object_or_404(Assets, pk=asset_id)
        asset_instance.new_branch_id = asset.branch_id
        asset_instance.new_status = asset.status
        asset_instance.new_notes = asset.notes
        asset_instance.user_id = user.id
        asset_instance.asset_id = asset_id
        asset_instance.save()
        return HttpResponseRedirect(reverse('assets:asset_detail_view', args=(asset_id,)))
    else:
        return render(request, 'assets_form.html', {'branches': branches, 'asset': asset})
