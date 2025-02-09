from django.urls import path
from moderator_panel import views

urlpatterns = [
    path('moderators-panel/', views.ModeratorPanelView.as_view(), name='moderators_panel'),
    path('product_checked/<int:pk>/', views.check_product, name='product_checked'),
]