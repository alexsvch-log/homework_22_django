# catalog/urls.py
from django.urls import path
from .views import (ProductListView, ProductDetailView, ContactsFormView, ProductCreateView, SuccessTemplateView,
                    ProductUpdateView, ProductDeleteView)


app_name = "catalog"

urlpatterns = [
    path('home/', ProductListView.as_view(), name='home'),
    path('contacts/', ContactsFormView.as_view(), name='contacts'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),

    # Страница успеха (если у вас настроен success_view, замените на свой класс или TemplateView)
    path('success/', SuccessTemplateView.as_view(), name='success'),
    # НОВЫЕ ПУТИ ДЛЯ ПОЛНОГО CRUD ТОВАРОВ:
    path('product/edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
