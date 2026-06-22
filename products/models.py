from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#---Authentication--User
class UserModel(AbstractUser):
    full_name = models.CharField(max_length=255, null=True)
    
    def __str__(self):
        return f"{self.username}---{self.full_name}"

#---CRUD--model
class ProductModel(models.Model):
    STATUS = [
        ('In-Stock' , 'In-Stock'),
        ('Out-Stock' , 'Out-Stock')
    ]
    name = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    price = models.FloatField(null=True)
    product_image = models.ImageField(upload_to='media/products', null=True)
    production_date = models.DateField(null=True)
    status = models.CharField(max_length=50, choices=STATUS, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        null=True,
        related_name='p_m'
    )
    
    def __str__(self):
        return f"{self.name}---{self.price}"
