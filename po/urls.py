from django.urls import path
from . import views
from .views import CreateView, DetailView


app_name = 'po'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:po_id>/process/', views.process_po, name='process_po'),

]
