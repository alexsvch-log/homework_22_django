from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render


def home_view(request: HttpRequest):
    if request.method == "GET":
        return render(request, "catalog/home.html")
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

    return render(request, "catalog/contacts.html")


def success_view(request: HttpRequest):
    # Достаем данные из сессии (.pop() прочитает данные и сразу сотрет их, чтобы не засорять память)
    context = {
        "name": request.session.pop("name", "Гость"),
    }
    return render(request, "catalog/success.html", context)
