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

    if request.method == "POST":
        # Извлекаем данные из полей формы
        name = request.POST.get("name")
        description = request.POST.get("description")
        price = request.POST.get("price")
        category_id = request.POST.get("category")
        image = request.FILES.get("image")  # Картинки берутся из request.FILES!

        # Находим объект категории по выбранному ID
        category = Category.objects.get(pk=category_id)

        # Создаем и сохраняем новый товар в базу данных PostgreSQL
        Product.objects.create(
            name=name,
            description=description,
            price=price,
            category=category,
            image=image
        )

        # После успешного создания перенаправляем менеджера на главную страницу каталога
        return redirect("catalog:home")

    # Если метод GET, просто отдаем страницу с формой
    context = {
        "categories": categories
    }
    return render(request, "catalog/product_form.html", context)
