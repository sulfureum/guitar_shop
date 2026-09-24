from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop/', views.shop_page, name='shop'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]