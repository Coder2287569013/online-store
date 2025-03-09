from django.db import models

# Create your models here.

class ChangeRequest(models.Model):
    seller = models.ForeignKey('auth_sys.CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey('store_content.Product', on_delete=models.CASCADE)
    message = models.TextField()

    def __str__(self):
        return f"Request change of {self.product}"
    
    class Meta:
        permissions = [
            ('can_request_change', 'Can request change'),
        ]