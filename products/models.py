# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal  # ✅ Added

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]  # ✅ Updated
    )
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, 
        related_name='products',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} (${self.price})"

    def reduce_stock(self, quantity):
        """Reduce stock by given quantity"""
        if self.stock < quantity:
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.save()
