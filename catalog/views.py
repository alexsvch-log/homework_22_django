from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required

from .models import ContactInfo  # Импортируем нашу новую модель контактов
from .models import Product, Category

# def home_view(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, "catalog/home.html")
#     return HttpResponseNotAllowed(["GET"])


def home_view(request: HttpRequest):
    if request.method == "GET":
        # Выбираем последние 5 товаров, сортируя по дате от новых к старым
        all_products = Product.objects.all()

        # 2. Настраиваем пагинатор: выводим, например, по 8 товаров на страницу
        # (8 отлично делится на сетку из 4 колонок Bootstrap)
        paginator = Paginator(all_products, 8)

        # Получаем номер текущей страницы из URL-адреса (например, /?page=2)
        page_number = request.GET.get('page')

        # Получаем товары конкретно для этой страницы
        page_obj = paginator.get_page(page_number)

        # # Выводим их в консоль (терминал PyCharm)
        # print("\n--- ПОСЛЕДНИЕ 5 ДОБАВЛЕННЫХ ТОВАРОВ ---")
        # for product in latest_products:
        #     print(f"ID: {product.id} | {product.name} | Цена: {product.price}")
        # print("---------------------------------------\n")

        # 3. Передаем ВСЕ товары в контекст шаблона. Передаем page_obj в контекст вместо all_products.
        context = {'page_obj': page_obj}
        return render(request, "catalog/home.html", context)

    return HttpResponseNotAllowed(["GET"])


def contacts_view(request: HttpRequest):
    if request.method == "POST":
        # Получение данных из формы
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        # Здесь мы можем сохранить данные в базу или отправить на email, но печатаем в консоль, просто так
        print(f"Новое сообщение: {name}, {email}, {phone}, {message}")

        # Если захоти просто отправить ответ без создания отдельной страницы с помощью библиотеки HttpResponse
        # return HttpResponse("Данные отправлены!")

        # Сохраняем имя в сессию, чтобы success_view мог его оттуда забрать
        request.session["name"] = name
        # Перенаправляем на страницу "Успех" и передаем имя в параметрах (опционально)
        return redirect("catalog:success")

    # Сюда программа попадает, если метод GET (обычное открытие страницы)
    # Забираем из базы самую первую (единственную) запись с контактными данными
    contact_data = ContactInfo.objects.first()

    # Передаем её в context для HTML-шаблона
    context = {"contact": contact_data}
    return render(request, "catalog/contacts.html", context)


def success_view(request: HttpRequest):
    # Достаем данные из сессии (.pop() прочитает данные и сразу сотрет их, чтобы не засорять память)
    context = {
        "name": request.session.pop("name", "Гость"),
    }
    return render(request, "catalog/success.html", context)


def product_detail_view(request: HttpRequest, pk: int):
    # Пытаемся найти товар по ID (pk). Если товара нет в базе — вернем чистую ошибку 404
    product = get_object_or_404(Product, pk=pk)

    # Передаем весь объект товара в шаблон
    context = {
        'product': product
    }
    return render(request, "catalog/product_info.html", context)

@staff_member_required  # Доступ только для администраторов и персонала магазина!
def product_create_view(request):
    # Нам понадобятся все категории, чтобы менеджер мог выбрать нужную в выпадающем списке
    categories = Category.objects.all()
    error_message = None  # Переменная для хранения текста ошибки

    if request.method == "POST":
        # Извлекаем данные из полей формы и сразу очищаем их от случайных крайних пробелов с помощью .strip()
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()
        price = request.POST.get("price", "").strip()
        category_id = request.POST.get("category")
        image = request.FILES.get("image")  # Картинки берутся из request.FILES!

        # 1. ЗАЩИТА: Проверяем, что обязательные текстовые поля не пустые
        if not name or not description or not price or not category_id:
            error_message = "Пожалуйста, заполните все обязательные поля формы!"

        else:
            try:
                # ЗАЩИТА: Проверяем, что цена — это корректное положительное число
                price_value = float(price)
                if price_value <= 0:
                    error_message = "Цена товара должна быть больше нуля!"
                else:
                    # ЗАЩИТА: Безопасно ищем категорию в базе
                    category = Category.objects.get(pk=category_id)

                    # Если все проверки пройдены — сохраняем в PostgreSQL
                    Product.objects.create(
                        name=name,
                        description=description,
                        price=price_value,
                        category=category,
                        image=image
                    )
                    return redirect("catalog:home")

            except ValueError:
                error_message = "Некорректный формат цены. Введите число (например, 1500.50)!"
            except Category.DoesNotExist:
                error_message = "Выбранная категория не существует в базе данных!"

    # Если это GET-запрос или если сработала одна из защит (появился error_message)
    context = {
        "categories": categories,
        "error": error_message  # Передаем текст ошибки в HTML
    }
    return render(request, "catalog/product_form.html", context)
