from django.urls import path
from auth_sys import views

urlpatterns = [
    path('signup/', views.CustomUserCreateView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('customize-profile/<int:pk>', views.CustomUserUpdateView.as_view(), name='customize_profile'),
    path('review/<int:seller_id>/<int:product_id>/', views.CreateReviewView.as_view(), name='review'),
    path('profile/<int:pk>', views.CustomUserProfileView.as_view(), name='profile')
]