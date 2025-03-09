from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from store_content.models import Product
from .forms import ChangeRequestForm
from .models import ChangeRequest
from django.views.generic import ListView, UpdateView, CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required

class ModeratorPanelView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'store_content.can_check_products'
    model = Product
    template_name = 'moderator_panel/main.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(unavailable=True)

class ModeratorChangeRequestView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'moderator_panel.can_request_change'
    form_class = ChangeRequestForm
    template_name = 'moderator_panel/change_request.html'
    success_url = reverse_lazy('moderators_panel')
    
    def form_valid(self, form):
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        form.instance.seller = product.seller
        form.instance.product = product
        response = super().form_valid(form)
        
        return response

@login_required
@permission_required('store_content.can_check_products')
def check_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.unavailable = False
    product.save()
    ChangeRequest.objects.filter(product=product).delete()

    return redirect('moderators_panel')