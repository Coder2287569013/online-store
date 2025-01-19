from django.urls import path
from store_content import views

urlpatterns = [
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/create/cities/', views.get_cities, name='get_cities'),
]