[4. Building a Social Website](#4-building-a-social-website)
---

- [Using the Django authentication framework](#using-the-django-authentication-framework)
- [Using Django’s built-in authentication views](#using-djangos-built-in-authentication-views)


# 4. Building a Social Website
- ## Using the Django authentication framework
    - ### Creating a login view
        > Create a new forms.py file in the account app
        ```python
            from django import forms  
            class LoginForm(forms.Form):

                username = forms.CharField()
                password = forms.CharField(widget=forms.PasswordInput)
        ```
        > Edit the views.py file of the account app
        ```python
            from django.contrib.auth import authenticate, login
            from django.http import HttpResponse
            from django.shortcuts import render
            from .forms import LoginForm

            def user_login(request):
                if request.method == 'POST':
                    form = LoginForm(request.POST)
                    if form.is_valid():
                        cd = form.cleaned_data
                        user = authenticate(
                            request,
                            username=cd['username'],
                            password=cd['password']
                        )
                        if user is not None:
                            if user.is_active:
                                login(request, user)
                                return HttpResponse('Authentication successfully')
                            else:
                                return HttpResponse('Disabled account')
                        else:
                            return HttpResponse('Invalid login')
                else:
                    form = LoginForm()
                return render(request, 'account/login.html', {'form': form})
        ```
        > Create a new urls.py file in account app
        ```python
            from django.urls import path
            from . import views

            urlpatterns = [
                path('login/', views.user_login, name='login'),

            ]
        ```
        > Edit the main urls.py file located in bookmarks
        ```python
            from django.contrib import admin
            from django.urls import include, path

            urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('account.urls')),
            ]
        ```
        > Create templates/base.html
        ```html
        {% load static %}
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{% block title %}{% endblock %}</title>
            <link rel="stylesheet" href="{% static "css/base.css" %}">
        </head>
        <body>
            <div id="header">
                <span class="logo">
                    Bookmarks
                </span>
            </div>
            <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        
        </body>
        </html>
        ```
        > Create template/account/login.html
        ```html
            {% extends "base.html" %}

            {% block title %}Log-in{% endblock %}

            {% block content %}
                <h1>Log-in</h1>
                <p>Please, use the following form to log-in:</p>
                <form action="" method="post">
                    {{ form.as_p }}
                    {% csrf_token %}
                    <p><input type="submit" value="Log in"></p>
                </form>
            {% endblock %}
        ```
- ## Using Django’s built-in authentication views
    > Django provides the following class-based to deal with authentication. All of them are located  \
    in  `django.contrib.auth.views`
    - `LoginView`: Handles a login form and logs in a user
    - `LogoutView`: Logs out a user
    > Django provides the following views to handle password changes:
    - `PasswordChangeView`: Handles a form to change the user's password
    - `PasswordChangeDoneView`: The success view that the user is redirected to after a successful password change
    > Django also includes the following views to allow users reset their password:
    - `PasswordResetView`: Allows users to reset their password. It generates a one-time-use link with a token and sends it to a user's email account
    - `PasswordResetDoneView`: Tells users that an email--including a ling to reset their password--has been sent to them
    - `PasswordResetConfirmView`: Allows users to set a new password
    - `PasswordResetCompleteView`: The success view that the user is redirect to after successfully resetting their password
    - ## Login and logout views
        > Edit the urls.py file of the account app
        ```python
            from django.contrib.auth import views as auth_views
            from django.urls import path
            from . import views

            urlpatterns = [
                # previous Login url
                # path('login/', views.user_login, name='login'),
                # login / logout urls
                path('login/', auth_views.LoginView.as_view(), name='login'),
                path('logout/', auth_views.LogoutView.as_view(), name='logout'),
            ]
        ```
        > Create a new file inside the templates/registration/ dir, name it login.html
        ```html
        {% extends "base.html" %}

        {% block title %}Log-in{% endblock %}

        {% block content %}
            <h1>Log-in</h1>
            {% if form.errors %}
            <p>
                Your username and password didn't match.
                Please try again.
            </p>
            {% else %}
              <p>Please, use the following form to log-in:</p>
            {% endif %}
            <div class="login-form">
                <form action="{% url "login" %}" method="post">
                    {{ form.as_p }}
                    {% csrf_token %}
                    <input type="hidden" name="next" value="{{ next }}">
                    <p><input type="submit" value="Log-in"></p>
                </form>
            </div>
        {% endblock %}
        ```
        > Create a logged_out.html template inside the templates/registration/
        ```html
        {% extends "base.html" %}

        {% block title %}Logged out{% endblock %}
        
        {% block content %}
            <h1>Logged out</h1>
            <p>
                You have been successfully logged out.
                You can <a href="{% url "login" %}">Log-in again</a>
            </p>
        {% endblock %}
        ```
        > Edit the views.py file of the account app
        ```python
            from django.contrib.auth.decorators import login_required

            @login_required
            def dashboard(request):
                return render(
                    request,
                    'account/dashboard.html',
                    {'section': 'dashboard'}
                )
        ```
        > Create a new file inside the template/account/ dir and name it dashboard.html
        ```html
        {% extends "base.html" %}

        {% block title %}Dashboard{% endblock %}

        {% block content %}
            <h1>Dashboard</h1>
            <p>Welcome to your dashboard.</p>
        {% endblock %}
        ```
        > Edit the account/urls.py
        ```python
            path('', views.dashboard, name='dashboard'),
        ```
        > Edit the bookmarks/settings.py
        ```python
            LOGIN_REDIRECT_URL = 'dashboard'
            LOGIN_URL = 'login'
            LOGOUT_URL = 'logout'
        ```
        > Edit the template/base.html
        ```html
        {% load static %}
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{% block title %}{% endblock %}</title>
            <link href="{% static "css/base.css" %}" rel="stylesheet">
        </head>
        <body>
            <div id="header">
                <span class="logo">Bookmarks</span>
                {% if request.user.is_authenticated %}
                    <ul class='menu'>
                        <li {% if section == 'dashboard' %}class="selected"{% endif %}>
                            <a href="{% url "dashboard" %}">My dashboard</a>
                        </li>
                        <li {% if section == 'images' %}class="selected"{% endif %}>
                            <a href="#">Images</a>
                        </li>
                            <li {% if section == 'people' %}class="selected"{% endif %}>
                            <a href="#">People</a>
                        </li>
                    </ul>
                {% endif %}
                <span class="user">
                    {% if request.user.is_authenticated %}
                        Hello {{ request.user.first_name|default:request.user.username }},
                        <form action="{% url "logout" %}" method="post">
                            <button type="submit">Logout</button>
                            {% csrf_token %}
                        </form>
                    {% else %}
                        <a href="{% url "login" %}">Log-in</a>
                    {% endif %}
                </span>
            </div>
            <div id="content">
                {% block content %}
                {% endblock %}
            </div>
        
        </body>
        </html>
        ```