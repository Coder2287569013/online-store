from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProductForm
from django.urls import reverse_lazy
from .models import Product, ProductImage, Category
from django.db import models
from cities_light.models import City
from django.views.generic import CreateView, DetailView, ListView, TemplateView

class MainView(TemplateView):
    template_name = 'base.html'

# Create your views here.
class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'store_content/product_create.html'
    success_url = reverse_lazy('signup')

    def form_valid(self, form):
        form.instance.seller = self.request.user
        response = super().form_valid(form)
        images = self.request.FILES.getlist('images')

        for image in images:
            ProductImage.objects.create(product=self.object, image=image)
        
        return response

class ProductDetailView(DetailView):
    model = Product
    template_name = 'store_content/product_view.html'
    context_object_name = 'product'

class ProductSearchListView(ListView):
    model = Product
    template_name = 'store_content/search_results.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('q')
        category = self.request.GET.get('category', 'all')
        if category == 'all':
            return Product.objects.filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(brand__icontains=query)
            )
        else:
            return Product.objects.filter(
                models.Q(title__icontains=query) |
                models.Q(description__icontains=query) |
                models.Q(brand__icontains=query),
                category__name=category
            )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q')
        return context

#API or API wannabe :\
def get_cities(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse([], safe=False)
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)

def search_suggestions(request):
    query = request.GET.get('q')
    categories = Category.objects.all()
    suggestions = []
    for category in categories:
        suggestions.append({
            'text': f'Search for {query} in {category.name}',
            'url': f'/search/?q={query}&category={category.name}'
        })
    suggestions.append({
        'text': f'Search for {query} in all categories',
        'url': f'/search/?q={query}&category=all'
    })

    return JsonResponse(suggestions, safe=False)