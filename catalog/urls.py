# catalog/urls.py
from django.urls import path
from .views import (
    ProductListView, ProductDetailView, ContactsFormView,
    ProductCreateView, SuccessTemplateView, ProductUpdateView,
    ProductDeleteView, UnpublishProductView
)

app_name = "catalog"

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsFormView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),

    # Страница успеха
    path('success/', SuccessTemplateView.as_view(), name='success'),

    # ПУТИ ДЛЯ ПОЛНОГО CRUD ТОВАРОВ И МОДЕРАЦИИ:
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/unpublish/<int:pk>/', UnpublishProductView.as_view(), name='product_unpublish'),
]
