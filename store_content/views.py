from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProductForm
from django.urls import reverse_lazy
from .models import Product, ProductImage
from cities_light.models import City
from django.views.generic import CreateView

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

#API or API wannabe :\
def get_cities(request):
    region_id = request.GET.get('region_id')
    if not region_id:
        return JsonResponse([], safe=False)
    cities = City.objects.filter(region_id=region_id).order_by('name')
    return JsonResponse(list(cities.values('id', 'name')), safe=False)