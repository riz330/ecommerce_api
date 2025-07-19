
# Create your models here.
from django.db import models
from django.conf import settings
from products.models import Product
from django.core.validators import MinValueValidator

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=settings.ORDER_STATUS,
        default='PENDING'
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipping_address = models.TextField()
    phone = models.CharField(max_length=20)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.email} - {self.status}"

    def update_status(self, new_status):
        """Update order status and notify user"""
        if new_status not in dict(settings.ORDER_STATUS).keys():
            raise ValueError("Invalid status")
        
        self.status = new_status
        self.save()
        self.notify_user()

    def notify_user(self):
        """Send real-time notification to user"""
        from .consumers import notify_user
        notify_user(self.user.id, {
            'type': 'order_update',
            'order_id': self.id,
            'status': self.status,
            'message': f'Your order status has been updated to {self.status}'
        })

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='order_items',
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('order', 'product')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order #{self.order.id})"

    def save(self, *args, **kwargs):
        """Calculate price based on product price"""
        if not self.price:
            self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.price for item in self.items.all())

    def __str__(self):
        return f"Cart of {self.user.email}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('cart', 'product')

    def save(self, *args, **kwargs):
        self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in cart"        