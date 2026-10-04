from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView
)

app_name = "blog"

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),                       # Список статей
    path('view/<int:pk>/', BlogDetailView.as_view(), name='detail'),     # Просмотр статьи
    path('create/', BlogCreateView.as_view(), name='create'),            # Создание
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),       # Редактирование
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),   # Удаление
]