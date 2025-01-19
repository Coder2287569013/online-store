from django.urls import path
from auth_sys import views

urlpatterns = [
    path('signup/', views.CustomUserCreateView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
]