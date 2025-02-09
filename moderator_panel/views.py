from django.shortcuts import get_object_or_404, render, redirect
from store_content.models import Product
from django.views.generic import ListView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required

class ModeratorPanelView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'store_content.can_check_products'
    model = Product
    template_name = 'moderator_panel/main.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(unavailable=True)

@login_required
@permission_required('store_content.can_check_products')
def check_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    product.unavailable = False
    product.save()

    return redirect('moderators_panel')