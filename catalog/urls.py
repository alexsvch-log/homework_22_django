# catalog/urls.py
from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    # Теперь эта страница доступна по адресу: catalog/home/
    path("home/", views.home_view, name="home"),
    # А эта страница по адресу: catalog/contacts/
    path("contacts/", views.contacts_view, name="contacts"),
    path("success/", views.success_view, name="success"),
    # НОВЫЙ ПУТЬ: <int:pk> принимает числовой ID товара и передает его в контроллер
    path('product/<int:pk>/', views.product_detail_view, name='product_detail'),
    path('product/create/', views.product_create_view, name='product_create'),
]
