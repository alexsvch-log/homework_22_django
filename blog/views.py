from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
# from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogEntry


# 1. Список статей (С разделением прав: админ видит черновики, гость — только опубликованные)
class BlogListView(ListView):
    model = BlogEntry
    template_name = 'blog/blog_list.html'
    context_object_name = 'articles'

    def get_queryset(self):
        # Если зашел администратор или контент-менеджер — показываем все статьи (включая черновики)
        if self.request.user.has_perm('blog.change_blogentry'):
            return BlogEntry.objects.all().order_by('-created_at')

        # Для обычных пользователей и гостей — только опубликованные
        return BlogEntry.objects.filter(is_published=True).order_by('-created_at')


# 2. Просмотр отдельной статьи: Увеличение счетчика просмотров)
class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/blog_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        # 1. Извлекаем объект статьи из базы данных
        obj = super().get_object(queryset)

        # 2. Увеличиваем счетчик просмотров на 1
        obj.views_count += 1
        obj.save()

        # 3. Проверяем, достигло ли количество просмотров ровно 100
        if obj.views_count == 100:
            send_mail(
                subject=f'Поздравляем! Статья "{obj.title}" стала популярной!',
                message=f'Ваша блоговая запись "{obj.title}" набрала ровно 100 просмотров в Online Strange Store! Так держать!',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['your_email@example.com'],  # Сюда можно вписать реальную почту
                fail_silently=True,
            )

        return obj


# 3. Создание статьи
class BlogCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogEntry
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.add_blogentry'

    # def test_func(self):
    #     return self.request.user.is_staff

# 4. Редактирование статьи
class BlogUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogEntry
    template_name = 'blog/blog_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    permission_required = 'blog.change_blogentry'

    # def test_func(self):
    #     return self.request.user.is_staff

    def get_success_url(self):
        return reverse('blog:detail', kwargs={'pk': self.object.pk})

# 5. Удаление статьи
class BlogDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogEntry
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
    permission_required = 'blog.delete_blogentry'

    # def test_func(self):
    #     return self.request.user.is_staff # Только для персонала

    # Метод удаления, использующий зелёное всплывающее сообщение об успешном удалении
    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f'Статья «{obj.title}» успешно удалена.')
        return super().delete(request, *args, **kwargs)