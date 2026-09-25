from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home'),
    path('shop/', views.shop_page, name='shop'),
    path('about/', views.about_page, name='about'),
    path('contact/', views.contact, name='contact'),
    path('search/', views.search, name='search'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('favorite/toggle/<int:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('favorites/', views.favorites_list, name='favorites_list'),
]