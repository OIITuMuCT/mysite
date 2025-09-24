[4. Building a Social Website](#4-building-a-social-website)
---

- [Using the Django authentication framework](#using-the-django-authentication-framework)
- [Using Django’s built-in authentication views](#using-djangos-built-in-authentication-views)
- [Creating a login view](#creating-a-login-view)
- [Using Django’s built-in authentication views](#using-djangos-built-in-authentication-views)
- [Login and logout views](#login-and-logout-views)
- [Change password views](#change-password-views)
- [Reset password views](#reset-password-views)
- [User registration](#user-registration)
- [Extending the user model](#extending-the-user-model)
- [Installing Pillow and serving media file](#installing-pillow-and-serving-media-file)
- [Creating migrations for the profile model](#creating-migrations-for-the-profile-model)

[5. Implementing Social Authentication](#5-implementing-social-authentication)
---

- [Using the messages framework]()
- [Building a custom authentication backend]()
  - [Preventing users from using an existing email]()
- [Adding social authentication with Python Social Auth]()
  - [Running the development server through HTTPS using Django Extensions]()
  - [Adding authentication using Google]()
  - [Creating a profile for users that register with social authentication]()

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
    - ## Change password views
      > Open the urls.py file of the account app

      ```python
        # ...
        path(
            'password-change/',
            auth_views.PasswordChangeView.as_view(),
            name='password_change'
        ),
        path(
            'password-change/done/',
            auth_views.PasswordChangeDoneView.as_view(),
            name='password_change_done'
        ),
      ```
      > Add a new file inside the templates/registration/ and name it `password_change_form.html`.
      ```html
        {% extends "base.html"%}

        {% block title%}Change your password{% endblock%}
        {% block content %}
        <h1>Change your password</h1>
        <p>Use the form below to change your password.</p>
        <form method="post">
            {{ form.as_p }}
            <p><input type="submit" value="Change"></p>
            {% csrf_token %}
        </form>
        {% endblock%}
      ```
      > Create another file in the same dir and name it `password_change_done.html`.
      ```html
        {% extends "base.html"%}

        {% block title %}Password changed{% endblock %}

        {% block content %}
        <h1>Password changed</h1>
        <p>Your password has been successfully changed.</p>
        {% endblock %}
      ```
    - ## Reset password views
      > Edit the `urls.py` file of the account app

      ```python
        urlpatterns = [
            # ...
            # reset password urls
            path('', auth_views.PasswordResetView.as_view(), name='password_reset'),
            path(
                'password-reset/done/',
                auth_views.PasswordResetDoneView.as_view(),
                name='password_reset_done'
            ),
            path(
                'password-reset/<uidb64>/<token>/',
                auth_views.PasswordResetConfirmView.as_view(),
                name='password_reset_confirm'
            ),
                path('password-reset/complete/',
                auth_views.PasswordResetCompleteView.as_view(),
                name='password_reset_complete'
            ),
        ]
      ```
      > Add a new file to the account/templates/registration/ and name it `password_reset_form.html`.
      ```html
        {% extends "base.html" %}

        {% block title %}Reset your password{% endblock %}

        {% block content %}
          <h1>Forgotten your password?</h1>
          <p>Enter your e-mail address to obtain a new password.</p>
          <form method="post">
            {{ form.as_p }}
            <p><input type="submit" value="Send e-mail"></p>
            {% csrf_token %}
          </form>
        {% endblock %}
      ```
      > Create another template in the same dir and name it `password_reset_email.html`.
      ```html
        Someone asked for password reset for email {{ email }}. Follow the link below:
        {{ protocol }}://{{ domain }}{% url "password_reset_confirm" uidb64=uid token=token %}
        Your username, in case you've forgotten: {{ user.get_username }}
      ```
      > Create another file in same dir and name it `password_reset_done.html`.
      ```html
        {% extends "base.html" %}

        {% block title %}Reset your password{% endblock %}

        {% block content %}
            <h1>Reset your password</h1>
            <p>We've emailed you instructions for setting your password.</p>
            <p>If you don't receive an email, please make sure you've entered the address you registered with.</p>
        {% endblock %}
      ```
      > Create another template in the same dir and name it `password_reset_confirm.html`
      ```html
        {% extends "base.html" %}
        
        {% block title %}Reset your password{% endblock %}

        {% block content %}
          <h1>Reset your password</h1>
          {% if validlink %}
          <p>Please enter your new password twice:</p>
          <form method="post">
            {{ form.as_p }}
            {% csrf_token %}
            <p><input type="submit" value="Change my password" /></p>
          </form>
          {% else %}
            <p>The password reset link was invalid, possibly because it has already been used. Please request a new password reset.</p>
          {% endif %}
        {% endblock %}
      ```
      > Create another template and name it `password_reset_complete.html`.
      ```html
        {% extends "base.html" %}
        
        {% block title %}Password reset{% endblock %}
        
        {% block content %}
          <h1>Password set</h1>
          <p>Your password has been set. You can <a href="{% url "login" %}">log in now</a></p>
        {% endblock %}
      ```
      > Finally, edit `registration/login.html`.
      ```html
        # ...
        </form>
        <p>
          <a href="{% url "password_reset" %}">
            Forgotten your password?
          </a>
        </p>
      ```
      > Edit the settings.py
      ```python
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
      ```
      > Comment out the authentication URL patterns tha you added to the **urls.py** file account app and include `django.contrib.auth.urls`.
      ```python
        from django.urls import include, path
        from django.contrib.auth import views as auth_views
        from . import views

        urlpatterns = [
            # comment all path
            path('', include('django.contrib.auth.urls')),
            path('', views.dashboard, name='dashboard'),
        ]
      ```
    - ## User registration
        > Create UserRegistrationForm
        ```python 
            from django import forms
            from django.contrib.auth import get_user_model

            class LoginForm(forms.Form):
                username = forms.CharField()
                password = forms.CharField(widget=forms.PasswordInput)
        
        class UserRegistrationForm(forms.ModelForm):
            password = forms.CharField(
                label='Password',
                widget=forms.PasswordInput
            )
            password2 = forms.CharField(
                label='Repeat password',
                widget=forms.PasswordInput
            )
            class Meta:
                model = get_user_model()
                fields = ['username', 'first_name', 'email']
            
            def clean_password2(self):
                cd = self.cleaned_data
                if cd['password'] != cd['password2']:
                    raise forms.ValidationError("Password don't match.")
                return cd['password2']
        ```
        > Edit the view.py file of the account app
        ```python
            # ...
            from . import LoginForm, UserRegistrationForm

            # ...
            def register(request):
                if request.method == "POST":
                    user_form = UserRegistrationForm(request.POST)
                    if user_form.is_valid():
                        new_user = user_form.save(commit=False)
                        new_user.set_password(
                            user_form.cleaned_data['password']
                        )
                        new_user.save()
                        return render(
                            request,
                            'account/register_done.html',
                            {"new_user": new_user}
                        )
                else:
                    user_form = UserRegistrationForm()
                return render(
                    request,
                    'account/register.html',
                    {"user_form": user_form}
                )
      ```
      > Edit urls.py file of the account app
      ```python
      urlpatterns = [
            # ...
            path('', include('django.contrib.auth.urls')),
            path('', views.dashboard, name='dashboard'),
            path('register/', views.register, name='register'),
        ]
      ```
      > Finally, create a new template in the templates/account/ and name it register.html
      ```html
        {% extends "base.html" %}

        {% block title %}Create an account{% endblock %}

        {% block content %}
          <h1>Create an account</h1>
          <p>Please, sign up using the following form:</p>
          <form method="post">
            {{ user_form.as_p }}
            {% csrf_token %}
            <p><input type="submit" value="Create my account"></p>
          </form>
        {% endblock %}
      ```
      > Create an additional template file in the same dir and name it register_done.html
      ```html
          {% extends "base.html" %}
          {% block title %}Welcome{% endblock %}
          {% block content %}
            <h1>Welcome {{ new_user.first_name }}!</h1>
            <p>
            Your account has been successfully created.
            Now you can <a href="{% url "login" %}">log in</a>.
            </p>
          {% endblock %}
      ```
      > Edit the registration/login.html
      ```html
        <p>
          Please, use the following form to log-in.
          If you don't have an account <a href="{% url "register" %}">register here</a>.
        </p>
      ```
    - ## Extending the user model
      > Edit the models.py file of the account app
      ```python
        from django.db import models
        from django.conf import settings

        class Profile(models.Model):
            user = models.OneToOneField(
                settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE
            )
            date_of_birth = models.DateField(blank=True, null=True)
            photo = models.ImageField(
                upload_to='users/%Y/%m/%d',
                blank=True
            )
            def __str__(self):
                return f'Profile of {self.user.username}'
      ```
    - ## Installing Pillow and serving media file
      ```shell
        python -m pip install Pillow
      ```
      > Edit setting.py
      ```python
        MEDIA_URL = 'media/'
        MEDIA_ROOT = BASE_DIR / 'media'
      ```
      > Edit bookmarks/urls.py
      ```python
        from django.conf import settings
        from django.conf.urls.static import static
        from django.contrib import admin
        from django.urls import path, include
        
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('account/', include('account.urls')),
        ]
        if settings.DEBUG:
            urlpatterns += static(
                settings.MEDIA_URL,
                document_root=settings.MEDIA_ROOT
            )
      ```
    - ## Creating migrations for the profile model
      ```shell
        python manage.py makemigrations
        python manage.py migrate
      ```
      > Edit account/admin.py
      ```python
        from django.contrib import admin
        from .models import Profile
        
        @admin.register(Profile)
        class ProfileAdmin(admin.ModelAdmin):
            list_display = ['user', 'date_of_birth', 'photo']
            raw_id_fields = ['user']
      ```
      > python manage.py runserver

      > Edit account/forms.py
      ```python
        # ...
        from .models import Profile

        # ...
        class UserEditForm(forms.ModelForm):
            class Meta:
                model = get_user_model()
                fields = ['first_name', 'last_name', 'email']
        
        class ProfileEditForm(forms.ModelForm):
            class Meta:
                model = Profile
                fields = ['date_of_birth', 'photo'] 
      ```
      > Edit the account/views.py
      ```python
        from .models import Profile

        #...
            #...
                new_user.save()
                # Create the user profile
                Profile.objects.create(user=new_user)
                return ...
      ```
      > Edit the account/views.py
      ```python
        from django.contrib.auth import authenticate, login
        from django.contrib.auth.decorators import login_required
        from django.http import HttpResponse
        from django.shortcuts import render
        from .forms import (
            LoginForm,
            UserRegistrationForm,
            UserEditForm,
            ProfileEditForm
        )
        from .models import Profile
        # ...
        
        @login_required
        def edit(request):
        if request.method == 'POST':
            user_form = UserEditForm(
                instance=request.user,
                data=request.POST
            )
            profile_form = ProfileEditForm(
                instance=request.user.profile,
                data=request.POST,
                files=request.FILES
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
            return render(
                request,
                'account/edit.html',
                {
                    'user_form': user_form,
                    'profile_form': profile_form
                }
            )
      ```
      > Add the URL pattern to the account/urls.py 
      ```python
        path('edit/', views.edit, name='edit'),
      ```
      > Create a template for this view in the template/account/ dir and name it edit.html.
      ```html
        {% extends "base.html" %}

        {% block title %}Edit your account{% endblock %}

        {% block content %}
          <h1>Edit your account</h1>
          <p>You can edit your account using the following form:</p>
          <form method="post" enctype="multipart/form-data">
          {{ user_form.as_p }}
          {{ profile_form.as_p }}
          {% csrf_token %}
          <p><input type="submit" value="Save changes"></p>
          </form>
        {% endblock %}
      ```
      > Open the templates/account/dashboard.html
      ```html
        {% extends "base.html" %}
        {% block title %}Dashboard{% endblock %}
        {% block content %}
          <h1>Dashboard</h1>
          <p>
            Welcome to your dashboard. You can <a href="{% url "edit" %}">edit your
            profile</a> or <a href="{% url "password_change" %}">change your password</a>.
          </p>
        {% endblock %}
      ```

# 5. Implementing Social Authentication
  - ## Using the messages framework
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
        {% if messages %}
        <ul class="messages">
            {% for message in messages %}
            <li class="{{ message.tags }}">
                {{ message|safe }}
                <a href="#" class="close">x</a>
            </li>
            {% endfor %}
        </ul>
        {% endif %}
        <div id="content">
            {% block content %}
            {% endblock %}
        </div>
    
    </body>
    </html>
    ```
    > Edit the account/views.py
    ```python
    from django.contrib import messages
    # ...
    @login_required
    def edit(request):
        if request.method == "POST":
            user_form = UserEditForm(
                instance = request.user,
                data=request.POST
            )
            profile_form = ProfileEditForm(
                instance=request.user.profile,
                data=request.POST,
                files=request.FILES
            )
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                message.success(
                    request,
                    'Profile updated successfully'
                )
            else:
                message.error(request, 'Error updating your profile')
        else:
            user_form = UserEditForm(instance=request.user)
            profile_form = ProfileEditForm(instance=request.user.profile)
        
    ```
  - ## Building a custom authentication backend
    > Create a new file inside the account app dir and name it authentication.py.
    ```python
    from django.contrib.auth.models import User

    class EmailAuthBackend:
        """ 
        Authenticate using an e-mail address.
        """

        def authenticate(self, request, username=None, password=None):
            try:
                user = User.objects.get(email=username)
                if user.check_password(password):
                    return user
                return None
            except (User.DoesNotExist, UserMultipleObjectsReturned):
                return None

        def get_user(self, user_id):
            try:
                return User.objects.get(pk=user_id)
            except User.DoesNotExist:
                return None
    ```
    > Edit the settings.py
    ```python
        AUTHENTICATION_BACKENDS = [
            'django.contrib.auth.backends.ModelBackend',
            'account.authentication.EmailAuthBackend',
        ]
    ```
    - ### Preventing users from using an existing email
    ```python
    class UserRegistrationForm(forms.ModelForm):
        password = forms.CharField(
            label='Password'
            widget=forms.PasswordInput
        )
        password2 = forms.CharField(
            label='Repeat password',
            widget=forms.PasswordInput
        )
        class Meta:
            model = User
            field = ['username', 'first_name', 'email']

        def clean_password2(self):
            cd = self.clean_data
            if cd['password'] != cd['password2']:
                raise forms.ValidationError("Passwords don't match.")
            return cd['password2']
        
        def clean_email(self):
            data = self.cleaned_data['email']
            if User.objects.filter(email=data).exists():
                raise forms.ValidationError('Email already in use.')
            return data

    class UserEditForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['firs_name', 'last_name', 'email']

        def clean_email(self):
            data = self.cleaned_data['email']
            qs = User.objects.exclude(
                id=self.instance.id
            ).filter(
                email=data
            )
            if qs.exists():
                raise forms.ValidationError('Email already in use.')
            return data
    ```
  - ## Adding social authentication with Python Social Auth
    ```shell
        python -m pip install social-auth-app-django==5.4.0
    ```
    ```python
        INSTALLED_APPS = [
            # ...
            'social_django',
        ]
    ```
    - ### Running the development server through HTTPS using Django Extensions
    - ### Adding authentication using Google
    - ### Creating a profile for users that register with social authentication