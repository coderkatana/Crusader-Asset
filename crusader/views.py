from django.shortcuts import render
from assets.models import Assets, UrAssets
from po.models import Po


def count(items):
    count = 0
    for item in items:
        count += 1
    return count


def index(request):
    pos = Po.objects.all()
    assets = Assets.objects.all()
    uras = UrAssets.objects.all()
    processed_pos = Po.objects.all().filter(processed=True)
    un_processed_pos = Po.objects.all().filter(processed=False)
    laptops = Assets.objects.all().filter(product_type__contains='laptop')
    printers = Assets.objects.all().filter(product_type__contains='printer')

    asset_count = count(assets)
    laptop_count = count(laptops)
    printer_count = count(printers)
    ura_count = count(uras)
    po_count = count(pos)
    processed_pos_count = count(processed_pos)
    un_processed_pos_count = count(un_processed_pos)

    context = {'assetCount': asset_count, 'laptop_count': laptop_count, 'printer_count': printer_count,
               'uraCount': ura_count,
               'poCount': po_count, 'processed_pos_count': processed_pos_count,
               'un_processed_pos_count': un_processed_pos_count}

    return render(request, 'index.html', context)
