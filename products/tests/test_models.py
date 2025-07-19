from django.test import TestCase
from products.models import Category, Product

class ProductModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )

    def test_create_product(self):
        product = Product.objects.create(
            name='Smartphone',
            description='Latest smartphone',
            price=999.99,
            stock=10,
            category=self.category
        )
        self.assertEqual(product.name, 'Smartphone')
        self.assertEqual(product.category.name, 'Electronics')
        self.assertEqual(product.stock, 10)

    def test_product_str(self):
        product = Product.objects.create(
            name='Laptop',
            price=1299.99,
            stock=5,
            category=self.category
        )
        self.assertEqual(str(product), 'Laptop ($1299.99)')