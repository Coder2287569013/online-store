from django.urls import path
from store_content import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/create/cities/', views.get_cities, name='get_cities'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_view'),
    path('search/', views.ProductSearchListView.as_view(), name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
]