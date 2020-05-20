from django.contrib import admin
from django.urls import path, include
from assets import views

app_name = "assets"
urlpatterns = [
    path('add/', views.add_view, name='asset_add'),
    path('ur/<int:ura_id>/add/', views.ura_to_asset_view, name='ura_asset_add'),
    path('list/', views.IndexView.as_view(), name='asset_list'),
    path('ur/list/', views.UrAView.as_view(), name='ur_asset_list'),
    path('<int:asset_id>/', views.asset_detail_view, name='asset_detail_view'),
    path('<int:asset_id>/update', views.asset_update_view, name='asset_update_view'),
    path('export/$', views.asset_export, name='asset_export'),

]
