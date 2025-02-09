from django.db import models
from cities_light.models import Country, City, Region

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):
    seller = models.ForeignKey(
        'auth_sys.CustomUser',
        on_delete=models.CASCADE,
        related_name='product'
    )
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    unavailable = models.BooleanField(default=True)    

    def __str__(self):
        return self.title
    
    class Meta:
        permissions = [
            ('can_check_products', 'Can check products'),
        ]


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.product.title


class ChatRoom(models.Model):
    seller = models.ForeignKey('auth_sys.CustomUser', on_delete=models.CASCADE, related_name='seller_room')
    buyer = models.ForeignKey('auth_sys.CustomUser', on_delete=models.CASCADE, related_name='buyer_room')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('seller', 'buyer', 'product')

    def __str__(self):
        return f'{self.seller.username} - {self.buyer.username} - {self.product.title}'

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey('auth_sys.CustomUser', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.author.username} - {self.room.product.title}'

class SavedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth_sys.CustomUser', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('product', 'user') 

    def __str__(self):
        return f"{self.user.username} saved {self.product.name}"