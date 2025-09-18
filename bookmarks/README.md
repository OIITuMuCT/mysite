[4. Building a Social Website](#4-building-a-social-website)
---

- [Using the Django authentication framework](#using-the-django-authentication-framework)


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
              ==path('', include('account.urls')),==
            ]