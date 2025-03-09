from django.urls import path
from store_content import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>', views.ProductUpdateView.as_view(), name="product_update"),
    path('product/create/cities/', views.get_cities, name='get_cities'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_view'),
    path('product/delete/<int:pk>', views.ProductDeleteView.as_view(), name='product_delete'),
    path('search/', views.ProductSearchListView.as_view(), name='search'),
    path('search/suggestions/', views.search_suggestions, name='search_suggestions'),
    path('chat/<int:product_id>/<int:buyer_id>/', views.ChatRoomView.as_view(), name='chat'),
    path('product/save/<int:pk>/', views.save_product, name='save_product'),
    path('product/saved/', views.SavedProductsView.as_view(), name='saved_products'),
    path('products/', views.ProductsListView.as_view(), name='all_products'),
    path('products/<int:category_id>', views.ProductsListView.as_view(), name='product_by_category')
]