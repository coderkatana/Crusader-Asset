import csv

from nms.models import nwData, Isp
from po.models import Branch, Vendor
from .models import nwData
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import (CreateView, DeleteView, DetailView, ListView, UpdateView)


class NmsListView(ListView):
    model = nwData
    template_name = 'nms_list.html'



def add_view(request):
    branches = Branch.objects.all()
    isps = Isp.objects.all()
    if request.method == 'POST':
        nms_data = nwData()
        nms_data.branch_id = request.POST.get('branch_dropdown')
        nms_data.isp_id = request.POST.get('isp_dropdown')
        nms_data.data = request.POST.get('data')
        nms_data.speed = request.POST.get('speed')
        nms_data.cost = request.POST.get('cost')
        nms_data.last_recharge = request.POST.get('last_recharge')
        nms_data.save()
        return HttpResponseRedirect(reverse('nms:nms_detail_view', args=(nms_data.id,)))
    else:
        return render(request, 'add_nms_data.html', {'branches':branches, 'isps':isps})


def nms_detail_view(request, nms_id):
    nms = get_object_or_404(nwData, pk=nms_id)
    # asset_histories = AssetHistory.objects.filter(asset_id=asset_id).order_by('-modified_at')
    return render(request, 'nw_data_detail_view.html', {'nms': nms})

def nms_update_view(request, nms_id):
    nms = get_object_or_404(nwData, pk=nms_id)
    branches = Branch.objects.all()
    isps = Isp.objects.all()

    if request.method == 'POST':
        user = request.user
        print(user)
        nms.isp_id = request.POST.get('isp_dropdown')
        nms.data = request.POST.get('data')
        nms.speed = request.POST.get('speed')
        nms.cost = request.POST.get('cost')

        # nms.last_recharge = request.POST.get('last_recharge')
        nms.save()
        return HttpResponseRedirect(reverse('nms:nms_detail_view', args=(nms_id,)))
    else:
        return render(request, 'nms_update.html', {'branches':branches, 'isps':isps, 'nms':nms})

def nms_export(request):
    pass