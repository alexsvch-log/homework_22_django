from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render

from .models import ContactInfo  # Импортируем нашу новую модель контактов
from .models import Product

# def home_view(request: HttpRequest):
#     if request.method == "GET":
#         return render(request, "catalog/home.html")
#     return HttpResponseNotAllowed(["GET"])


def home_view(request: HttpRequest):
    if request.method == "GET":
        # Выбираем последние 5 товаров, сортируя по дате от новых к старым
        latest_products = Product.objects.all().order_by("-created_at")[:5]

        # Выводим их в консоль (терминал PyCharm)
        print("\n--- ПОСЛЕДНИЕ 5 ДОБАВЛЕННЫХ ТОВАРОВ ---")
        for product in latest_products:
            print(f"ID: {product.id} | {product.name} | Цена: {product.price}")
        print("---------------------------------------\n")

        # Также передадим их в контекст (может пригодиться для вывода на саму страницу)
        context = {"products": latest_products}
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
