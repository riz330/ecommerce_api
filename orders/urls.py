from django.urls import path
from .views import (
    OrderListCreateView,
    OrderRetrieveView,
    OrderUpdateStatusView,
    CartItemView,
    CartView
)

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/items/', CartItemView.as_view(), name='cart-items'),
    path('orders/', OrderListCreateView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderRetrieveView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', OrderUpdateStatusView.as_view(), name='order-status'),
]