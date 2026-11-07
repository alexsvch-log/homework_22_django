from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.conf import settings
from .forms import UserRegisterForm, UserLoginForm
from django.views.generic import UpdateView
from .forms import UserProfileForm
from .models import User


# 1. Контроллер Регистрации
class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')  # После регистрации отправляем на страницу входа

    def form_valid(self, form):
        # Сохраняем нового пользователя в базу данных
        user = form.save()

        # ТЗ 2: Логика отправки приветственного письма
        send_mail(
            subject='Добро пожаловать в Online Strange Store!',
            message=f'Здравствуйте! Спасибо за регистрацию на нашем сайте. Ваш логин для входа: {user.email}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        return super().form_valid(form)


# 2. Контроллер Входа (Авторизации)
class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'


# 3. Контроллер Выхода из системы
class UserLogoutView(LogoutView):
    next_page = reverse_lazy('catalog:home')  # После выхода отправляем на главную каталога

class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:home')

    def get_object(self, queryset=None):
        # Этот метод заставляет Django редактировать именно того пользователя, который сейчас вошел на сайт
        return self.request.user
