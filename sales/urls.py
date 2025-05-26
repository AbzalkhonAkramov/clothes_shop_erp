from django.urls import path
from . import views

urlpatterns = [
    path('', views.sales_dashboard, name='sales_dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('add/', views.add_sale, name='add_sale'),
]
