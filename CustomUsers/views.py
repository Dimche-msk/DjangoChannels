from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages # Для отображения сообщений пользователю

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Добро пожаловать, {username}!")
                # Перенаправляем на главную страницу или другую страницу после входа
                # Например, на страницу, где будет использоваться WebSocket
                return redirect('/') #
            else:
                messages.error(request, "Неверное имя пользователя или пароль.")
        else:
            messages.error(request, "Неверное имя пользователя или пароль.")
    else:
        # Если пользователь уже аутентифицирован, перенаправляем его
        if request.user.is_authenticated:
            return redirect('/') #
        form = AuthenticationForm()
    return render(request, 'CustomUsers/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST': # Рекомендуется делать logout через POST для безопасности
        auth_logout(request)
        messages.info(request, "Вы успешно вышли из системы.")
        return redirect('/login') # Перенаправляем на страницу входа
    # Если GET-запрос, можно показать страницу подтверждения или просто перенаправить
    # Для простоты, если это не POST, можно просто перенаправить на главную или страницу входа
    return redirect('/home') # Или 'login'

# Пример простой домашней страницы, куда можно перенаправить после входа
def home_view(request):
    return render(request, 'CustomUsers/home.html')
