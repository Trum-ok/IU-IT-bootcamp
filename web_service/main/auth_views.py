from typing import Literal

from django.shortcuts import redirect, render


def writer_login(request):
    return login(request, "writer")


def moderator_login(request):
    return login(request, "moderator")


def login(request, user_role: Literal["writer", "moderator"]):
    """
    Функция для авторизации пользователей и присваение им определенной роли
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(f"login: {username} {password}")
        # user = external_db.get_user(username, password)
        user = {"id": 123, "user_role": user_role}

        if user:
            request.session["user_id"] = user["id"]
            request.session["user_role"] = user["user_role"]
            return redirect("home")

        return render(
            request, "login.html"
        )

    return render(request, "login.html")


def logout(request):
    request.session.flush()
    return redirect("home")
