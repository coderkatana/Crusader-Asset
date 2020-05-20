from django.shortcuts import render
from django.http import HttpResponse
from . models import Product
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView



def index(request):
    model = Product
    template_name = 'productList.html'
    return render(request, 'productList.html', {'products': products})