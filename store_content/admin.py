from django.contrib import admin
from .models import Category, Product, ProductImage, ChatRoom, Message, SavedProduct
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(ChatRoom)
admin.site.register(Message)
admin.site.register(SavedProduct)