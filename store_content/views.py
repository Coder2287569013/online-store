from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from fuzzywuzzy import fuzz
from django.http import JsonResponse
from .forms import ProductForm, MessageForm
from django.urls import reverse_lazy
from .models import Product, ProductImage, Category, ChatRoom, SavedProduct
from auth_sys.models import Review
from django.db import models
from cities_light.models import City
from django.views.generic import CreateView, DetailView, ListView, TemplateView, DeleteView
from .mixins import UserIsOwnerMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator

class MainView(TemplateView):
    template_name = 'base.html'

# Create your views here.
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store_content/product_create.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')

        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        
        return response


class ProductDeleteView(UserIsOwnerMixin, DeleteView):
    model = Product
    template_name = 'store_content/product_confirm_delete.html'
    
    def get_success_url(self):
        user = self.request.user

        if user.groups.filter(name__in=['Admin', 'Moderators']).exists():
            return reverse_lazy('moderators_panel')
        else:
            return reverse_lazy('main')


class ProductDetailView(DetailView):
    model = Product
    template_name = 'store_content/product_view.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reviews = Review.objects.filter(user=context['product'].seller).values_list('rate', flat=True)
        rating = round(sum(reviews) / len(reviews), 1) if reviews else 0
        context['rating'] = rating
        return context


class ProductSearchListView(ListView):
    model = Product
    template_name = 'store_content/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q').strip()
        words = query.split()
        category = self.request.GET.get('category', 'all')

        if category == 'all':
            products = Product.objects.filter(unavailable=False)
        else:
            products = Product.objects.filter(category__name=category, unavailable=False)
        
        filtered_products = []
        for product in products:
            product_text = f"{product.title} {product.description} {product.brand}"
            for word in words:
                if fuzz.partial_ratio(word.lower(), product_text.lower()) > 60:
                    filtered_products.append(product)
                    break
        
        return filtered_products
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context


@method_decorator(login_required, name='dispatch')
class ChatRoomView(DetailView):
    model = ChatRoom
    template_name = 'store_content/chat_room.html'
    context_object_name = 'chat_room'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, pk=self.kwargs.get('product_id'))
        buyer_id = self.kwargs.get('buyer_id')

        if self.request.user == product.seller:
            chat = ChatRoom.objects.filter(seller=self.request.user, product=product, buyer_id=buyer_id).first()
        else:
            chat, created = ChatRoom.objects.get_or_create(
                buyer=self.request.user,
                seller=product.seller,
                product=product
            )

        return chat

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = MessageForm()
        return context

    def post(self, request, *args, **kwargs):
        chat = self.get_object()
        if not chat:  
            return JsonResponse({"error": "Chat room not found"}, status=404)

        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.room = chat  
            message.author = request.user  
            message.save()
            return redirect('chat', product_id=chat.product.id, buyer_id=chat.buyer.id)


class SavedProductsView(LoginRequiredMixin, ListView):
    model = SavedProduct
    template_name = 'store_content/saved.html'
    context_object_name = 'saved'

    def get_queryset(self):
        return SavedProduct.objects.filter(user=self.request.user)
    


    
#API or API wannabe :\
def get_cities(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse([], safe=False)
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

def search_suggestions(request):
    query = request.GET.get('q').strip()
    suggestions = []

    words = query.split()

    categories = Category.objects.none()

    for word in words:
        categories |= Category.objects.filter(
            models.Q(name__icontains=word) |
            models.Q(product__title__icontains=word) |
            models.Q(product__description__icontains=word) |
            models.Q(product__brand__icontains=word) &
            models.Q(product__unavailable=False)
        ).distinct()

    relevant_categories = categories.distinct()
          
    categories = Category.objects.all()
    for category in relevant_categories:
        suggestions.append({
            'text': f'Search for {query} in {category.name}',
            'url': f'/search/?q={query}&category={category.name}'
        })
    suggestions.append({
        'text': f'Search for {query} in all categories',
        'url': f'/search/?q={query}&category=all'
    })

    return JsonResponse(suggestions, safe=False)

@login_required
def save_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    SavedProduct.objects.create(
        product = product,
        user = request.user
    )

    return redirect('product_view', pk)