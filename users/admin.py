# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User  # Импортируем ваш класс User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 1. Список пользователей в таблице админки
    list_display = ("id", "email", "first_name", "last_name", "phone", "get_groups", "is_staff")

    # 2. Поля, по которым будет работать поиск
    search_fields = ("email", "first_name", "last_name", "phone")

    # 3. Фильтры справа в панели
    list_filter = ("groups","is_staff", "is_superuser", "is_active", "country")

    # 4. Сортировка списка по умолчанию
    ordering = ("email",)

    # 5. Переопределяем структуру полей внутри карточки пользователя.
    # ВАЖНО: полностью убираем 'username' и добавляем ваши новые поля.
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {"fields": ("first_name", "last_name", "avatar", "phone", "country")}
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # 6. Если вы будете создавать пользователя ЧЕРЕЗ админку,
    # стандартная форма тоже потребует email вместо username
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "first_name", "last_name"),
            },
        ),
    )

    # 7. Метод для вывода названий групп в таблице
    @admin.display(description="Группы")
    def get_groups(self, obj):
        groups = obj.groups.all()
        if groups:
            return ", ".join([group.name for group in groups])
        return "—"