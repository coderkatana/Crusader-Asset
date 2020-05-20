from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "nms"
urlpatterns = [
    path('add/', views.add_view, name='nms_add'),
    path('list/', views.NmsListView.as_view(), name='nms_list'),
    path('<int:nms_id>/', views.nms_detail_view, name='nms_detail_view'),
    path('<int:nms_id>/update', views.nms_update_view, name='nms_update_view'),
    path('export/$', views.nms_export, name='nms_export'),

]
