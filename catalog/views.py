from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin  # Импортируем миксин для проверки прав админа
from django.contrib import messages

from .models import Product, ContactInfo
from .forms import ProductForm, ContactForm


# 1. Главная страница  (Замена home_view)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # Имя переменной в цикле шаблона
    paginate_by = 8  # Встроенная пагинация Django!

    def get_queryset(self):
        # Возвращаем все товары, отсортированные по дате добавления
        return Product.objects.all().order_by('-created_at')


# 2. Страница контактов (Замена contacts_view)
class ContactsFormView(FormView):
    form_class = ContactForm
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:success')

    def get_context_data(self, **kwargs):
        # Передаем контактные данные компании из базы, как и раньше
        context = super().get_context_data(**kwargs)
        context['contact'] = ContactInfo.objects.first()
        return context

    def form_valid(self, form):
        # Этот метод вызывается, когда пользователь заполнил все поля без ошибок
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        phone = form.cleaned_data['phone']
        message = form.cleaned_data['message']

        # Печатаем чистое сообщение в консоль PyCharm
        print(f"Новое сообщение от {name} ({email}, {phone}): {message}")

        # Сохраняем имя в сессию для страницы успеха
        self.request.session["name"] = name

        return super().form_valid(form)


class SuccessTemplateView(TemplateView):
    template_name = "catalog/success.html"

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст от Django
        context = super().get_context_data(**kwargs)

        # Достаем данные из сессии, как в вашей исходной функции (.pop() прочитает и сотрет)
        context["name"] = self.request.session.pop("name", "Гость")

        return context


# 3. Страница товара (Замена product_detail_view)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_info.html'
    context_object_name = 'product'


# 4. Форма создания товара (Замена product_create_view)
class ProductCreateView(UserPassesTestMixin, CreateView):
    model = Product
    form_class = ProductForm  # Привязываем кастомную форму с валидацией
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    # Этот метод теперьзапустится и проверит статус админа
    def test_func(self):
        return self.request.user.is_staff

    # Метод form_valid оставляем, он сработает СРАЗУ ПОСЛЕ проверок из forms.py
    def form_valid(self, form):
        price = form.cleaned_data.get('price')
        if price and price <= 0:
            form.add_error('price', 'Цена товара должна быть больше нуля!')
            return self.form_invalid(form)

        return super().form_valid(form)

# Класс редактирования товара (тоже использует ProductForm)
class ProductUpdateView(UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        return self.request.user.is_staff

# Класс удаления товара
class ProductDeleteView(UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        return self.request.user.is_staff

    # Добавляем всплывающее уведомление
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Товар «{obj.name}» успешно удален из каталога.')
        return super().delete(request, *args, **kwargs)