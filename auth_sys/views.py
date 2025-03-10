from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from .models import CustomUser, Review
from moderator_panel.models import ChangeRequest
from store_content.models import Product, ChatRoom
from .forms import CustomUserCreationForm, CustomUserChangeForm, ReviewForm

# Create your views here.
class CustomUserCreateView(CreateView):
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'auth_sys/signup.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)

        return redirect('main')


class CustomLoginView(LoginView):
    template_name = 'auth_sys/login.html'
    success_url = reverse_lazy('main')

class CustomLogoutView(LogoutView):
    next_page = 'main'


class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = 'auth_sys/customize_profile.html'

    def form_valid(self, form):
        user = form.save(commit=False)

        if self.request.POST.get('avatar-clear', None): 
            user.avatar = 'avatars/default_avatar.png'
        elif 'avatar' in self.request.FILES:
            user.avatar = self.request.FILES['avatar']

        user.save()
        return redirect('main')
    

class CreateReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'auth_sys/review_create.html'
    
    def form_valid(self, form):
        seller_id = self.kwargs.get('seller_id')
        seller = get_object_or_404(CustomUser, pk=seller_id) 
        form.instance.user = seller 

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('product_view', kwargs={'pk': self.kwargs['product_id']})


class CustomUserProfileView(DetailView):
    model = CustomUser
    template_name = 'auth_sys/profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(user=context['user'])
        rating = round(sum(reviews.values_list('rate', flat=True)) / len(reviews), 1) if reviews else 0
        context['reviews'] = reviews
        context['rating'] = rating
        context['products'] = Product.objects.filter(seller=context['user'])
        context['chats'] = ChatRoom.objects.filter(Q(seller=context['user']) | Q(buyer=context['user']))
        context['changes'] = ChangeRequest.objects.filter(seller=context['user'])
        return context


class RatingView(ListView):
    model = Review
    template_name = 'auth_sys/rating.html'
    context_object_name = 'reviews'

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = self.get_queryset()
        rating = round(sum(reviews.values_list('rate', flat=True)) / len(reviews), 1) if reviews.exists() else 0
        context['rating'] = rating
        return context


class ProductsView(ListView):
    model = Product
    template_name = 'auth_sys/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        context['available_count'] = products.filter(unavailable=False).count()
        context['unavailable_count'] = products.filter(unavailable=True).count()
        return context


class ChatListView(ListView):
    model = ChatRoom
    template_name = 'auth_sys/chats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        return ChatRoom.objects.filter(Q(seller=self.request.user) | Q(buyer=self.request.user))


class ChangeRequestsView(ListView):
    model = ChangeRequest
    template_name = 'auth_sys/c_requests.html'
    context_object_name = 'requests'

    def get_queryset(self):
        return ChangeRequest.objects.filter(seller=self.request.user)