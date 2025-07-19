from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Product,Category
from orders.models import Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()

class CartTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@test.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Smartphone',
            price=999.99,
            stock=10,
            category=self.category
        )
        self.cart_url = reverse('cart')
        self.cart_items_url = reverse('cart-items')
        self.client.force_authenticate(user=self.user)

    def test_get_cart(self):
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['items'], [])

    def test_add_to_cart(self):
        data = {
            'product_id': self.product.id,
            'quantity': 2
        }
        response = self.client.post(self.cart_items_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CartItem.objects.count(), 1)

    def test_remove_from_cart(self):
        cart = Cart.objects.get(user=self.user)
        CartItem.objects.create(
            cart=cart,
            product=self.product,
            quantity=1,
            price=self.product.price
        )
        data = {
            'product_id': self.product.id
        }
        response = self.client.delete(self.cart_items_url, data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CartItem.objects.count(), 0)