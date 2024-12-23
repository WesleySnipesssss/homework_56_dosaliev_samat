from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView,
    ProductDeleteView, CategoryCreateView,
    add_to_cart, cart_view, remove_from_cart,
    remove_one_from_cart
)

urlpatterns = [
    path('', ProductListView.as_view(), name='products_view'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('products/add/', ProductCreateView.as_view(), name='product_add_view'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit_view'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete_view'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add_view'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove_one/<int:pk>/', remove_one_from_cart, name='remove_one_from_cart'),
    path('cart/remove/<int:pk>/', remove_from_cart, name='remove_from_cart'),
    path('cart/', cart_view, name='cart_view'),
]
