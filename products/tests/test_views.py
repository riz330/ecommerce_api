from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from products.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

class ProductViewTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            email='admin@test.com',
            password='adminpass123'
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            password='userpass123'
        )
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )
        self.product = Product.objects.create(
            name='Smartphone',
            description='Latest model',
            price=999.99,
            stock=10,
            category=self.category
        )
        self.list_url = reverse('product-list')
        self.detail_url = reverse('product-detail', args=[self.product.id])

    def test_list_products(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_product_as_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'name': 'Laptop',
            'description': 'High performance laptop',
            'price': '1499.99',
            'stock': 5,
            'category_id': self.category.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)

    def test_create_product_as_user(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'Tablet',
            'price': '499.99',
            'stock': 3,
            'category_id': self.category.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)