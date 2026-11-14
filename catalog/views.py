from django.contrib.auth.mixins import LoginRequiredMixin  # Импортируем миксин авторизации
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import UserPassesTestMixin  # Импортируем миксин для проверки прав
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views import View

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
class ProductDetailView(LoginRequiredMixin,DetailView):
    model = Product
    template_name = 'catalog/product_info.html'
    context_object_name = 'product'


# 4. Форма создания товара (Замена product_create_view)
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm  # Привязываем кастомную форму с валидацией
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    # Метод form_valid оставляем, он сработает СРАЗУ ПОСЛЕ проверок из forms.py
    def form_valid(self, form):
        price = form.cleaned_data.get('price')
        if price and price <= 0:
            form.add_error('price', 'Цена товара должна быть больше нуля!')
            return self.form_invalid(form)

        # Автоматически привязываем текущего пользователя как владельца
        product = form.save(commit=False)
        product.owner = self.request.user
        product.save()

        return super().form_valid(form)


# Класс редактирования товара (тоже использует ProductForm)
class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        # Получаем редактируемый товар и сверяем его владельца с текущим пользователем
        product = self.get_object()
        # Разрешаем редактирование создателю товара ИЛИ модератору (и админу)
        return self.request.user == product.owner or self.request.user.has_perm('catalog.can_unpublish_product')

# Класс удаления товара
class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:home')

    def test_func(self):
        product = self.get_object()
        # Разрешаем удаление автору товара ИЛИ пользователю с правом модератора
        return self.request.user == product.owner or self.request.user.has_perm('catalog.delete_product')

    # Добавляем всплывающее уведомление
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Товар «{obj.name}» успешно удален из каталога.')
        return super().delete(request, *args, **kwargs)


class UnpublishProductView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = False
        product.save()
        messages.success(request, f'Публикация товара «{product.name}» отменена.')
        return redirect('catalog:home')
