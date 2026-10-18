from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin # Замена декоратора для классов

from .models import Product, Category, ContactInfo


# 1. Главная страница (Замена home_view)
class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'  # Имя переменной в цикле шаблона
    paginate_by = 8  # Встроенная пагинация Django!

    def get_queryset(self):
        # Возвращаем все товары, отсортированные по дате добавления
        return Product.objects.all().order_by('-created_at')


# 2. Страница контактов (Замена contacts_view)
class ContactsTemplateView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем контактные данные в контекст страницы
        context['contact'] = ContactInfo.objects.first()
        return context

    def post(self, request, *args, **kwargs):
        # Обработка отправки формы обратной связи (как и было в FBV)
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        print(f"Новое сообщение: {name}, {email}, {phone}, {message}")

        request.session["name"] = name
        from django.shortcuts import redirect
        return redirect("catalog:success")


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
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'catalog/product_form.html'
    fields = ['name', 'description', 'price', 'category', 'image'] # Поля формы
    success_url = reverse_lazy('catalog:home') # Куда перенаправить после успеха

    # ГЛАВНОЕ УСЛОВИЕ: Этот метод проверяет, является ли пользователь админом/персоналом
    def test_func(self):
        return self.request.user.is_staff  # Возвращает True только для админов


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем категории для выпадающего списка
        context['categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        # В CBV встроенная валидация сама проверяет поля на пустоту (required)!
        # Добавим нашу кастомную проверку: цена должна быть больше нуля
        price = form.cleaned_data.get('price')
        if price and price <= 0:
            form.add_error('price', 'Цена товара должна быть больше нуля!')
            return self.form_invalid(form)

        return super().form_valid(form)
