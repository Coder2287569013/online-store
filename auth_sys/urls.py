from django.urls import path
from auth_sys import views

urlpatterns = [
    path('signup/', views.CustomUserCreateView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('customize-profile/<int:pk>/', views.CustomUserUpdateView.as_view(), name='customize_profile'),
    path('review/<int:seller_id>/<int:product_id>/', views.CreateReviewView.as_view(), name='review'),
    path('profile/<int:pk>/', views.CustomUserProfileView.as_view(), name='profile'),
    path('rating/<int:pk>/', views.RatingView.as_view(), name='rating'),
    path('user-products/<int:pk>/', views.ProductsView.as_view(), name='products-user'),
    path('user-chats/<int:pk>/', views.ChatListView.as_view(), name='user_chats'),
    path('user-crequests/<int:pk>/', views.ChangeRequestsView.as_view(), name='user_crequests')
]