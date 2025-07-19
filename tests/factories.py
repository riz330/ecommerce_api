import factory
from django.contrib.auth import get_user_model
from products.models import Category, Product
from orders.models import Order, OrderItem, Cart, CartItem

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@test.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpass123')

class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    description = factory.Faker('paragraph')

class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Sequence(lambda n: f'Product {n}')
    description = factory.Faker('paragraph')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    stock = factory.Faker('random_int', min=0, max=100)
    category = factory.SubFactory(CategoryFactory)

class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)

class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
    price = factory.LazyAttribute(lambda o: o.product.price * o.quantity)

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    status = 'PENDING'
    total_price = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    shipping_address = factory.Faker('address')
    phone = factory.Faker('phone_number')

class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_int', min=1, max=5)
    price = factory.LazyAttribute(lambda o: o.product.price * o.quantity)