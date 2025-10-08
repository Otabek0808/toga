from django.urls import path
from .views import (
    ProductListView,
    ProductAddView,
    ProductSellView,
    SoldProductListView,
    delete_product,
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('add/', ProductAddView.as_view(), name='product-add'),
    path('sell/<int:pk>/', ProductSellView.as_view(), name='product-sell'),
    path('sold/', SoldProductListView.as_view(), name='sold-product-list'),
    path('delete/<int:pk>/', delete_product, name='product-delete'),
]
