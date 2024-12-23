from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    ProductCreateView, ProductUpdateView,
    ProductDeleteView, CategoryCreateView
)

urlpatterns = [
    path('', ProductListView.as_view(), name='products_view'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_view'),
    path('products/add/', ProductCreateView.as_view(), name='product_add_view'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit_view'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete_view'),
    path('category/add/', CategoryCreateView.as_view(), name='category_add_view'),
]
