[12. Building an E-Learning Platform](#12-building-an-e-learning-platform)
<!-- Create models for the CMS -->
- [Setting up the e-learning project](#setting-up-the-e-learning-project)
- [Serving media files](#serving-media-files)
- [Building the courses models](#building-the-courses-models)
- [Registering the models in the administration site](#registering-the-models-in-the-administration-site)
<!-- Create fixtures for your models and apply them -->
- [Using fixtures to provide initial data for models](#using-fixtures-to-provide-initial-data-for-models)
<!-- User model inheritance to create data models for polymorphic content -->
- [Using model inheritance](#using-model-inheritance)
- [Creating the Content models](#creating-the-content-models)
<!-- - [Create custom models fields]() -->
- [Creating custom model fields](#creating-custom-model-fields)
<!-- - [Order course contents and modules]() -->
- [Adding ordering to Module and Content objects](#adding-ordering-to-module-and-content-objects)
<!-- - [Build authentication views for the CMS]() -->
- [Adding authentication views](#adding-authentication-views)



# 12. Building an E-Learning Platform
## Setting up the e-learning project
> python -m venv env/educa

> source env/educa/bin/activate

```shell
    python -m pip install Django~=5.0.4

    python -m pip install Pillow==10.3.0
    
    # Create a new project
    django-admin startproject educa
    cd educa
    django-admin startapp courses
```
> Edit the settings.py
```python
    INSTALLED_APPS = [
        'courses.apps.CoursesConfig',
        # ... 
    ]
```
## Serving media files
> Edit the settings.py
```python
    from django.conf import settings
    from django.conf.urls.static import static
    from django.contrib import admin
    from django.urls import path

    urlpatterns = [
        path('admin/', admin.site.urls),
    ]

    if settings.DEBUG:
        urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
```
## Building the courses models
```
Subject 1
    Course 1
        Module 1
            Content 1 (image)
            Content 2 (text)
        Module 2
            Content 3 (text)
            Content 4 (file)
            Content 5 (video)
        ...
```
> Edit the models.py file of the course app
```python
    from django.contrib.auth.models import User
    from django.db import models

    class Subject(models.Model):
        title = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200, unique=True)

        class Meta:
            ordering = ['title']

        def __str__(self):
            return self.title

    class Course(models.Model):
        owner = models.ForeignKey(
            User,
            related_name='courses_created',
            on_delete=models.CASCADE
        )
        subject = models.ForeignKey(
            Subject,
            related_name='courses',
            on_delete=models.CASCADE
        )
        title = models.CharField(max_length=200)
        slug = models.SlugField(max_length=200, unique=True)
        overview = models.TextField()
        created = models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering = ['-created']

        def __str__(self):
            return self.title

    class Module(models.Model):
        course = models.ForeignKey(
            Courses,
            related_name='modules',
            on_delete=models.CASCADE
        )
        title = models.CharField(max_length=200)
        description = models.TextField(blank=True)

        def __str__(self):
            return self.title
```
> These are the initial **Subject**, **Course**, and **Module** models. The Course model fields are as follows:
>  - owner: The instructor who created this course.
>  - subject: The subject that this course belongs to. It is a ForeignKey field that points to the Subject model.
>  - title: The title of the course.
>  - slug: The slug of the course. This will be used in URLs later.
>  - overview: A TextField column to store an overview of the course.
>  - created: The date and time when the course was created. It will be automatically set by Django when creating new objects because of auto_now_add=True.

```shell
    python manage.py makemigrations
    python manage.py migrate
```
## Registering the models in the administration site
```python
    from django.contrib import admin
    from .models import Subject, Course, Module

    @admin.register(Subject)
    class SubjectAdmin(admin.ModelAdmin):
        list_display = ['title', 'slug']
        prepopulated_fields = {'slug': ('title',)}

    class ModuleInline(admin.StakedInLine):
        model = Module

    @admin.register(Course)
    class CourseAdmin(admin.ModelAdmin):
        list_display = ['title', 'subject', 'created']
        list_filter = ['created', 'subject']
        search_fields = ['title', 'overview']
        prepopulated_fields = {'slug': ('title',)}
        inlines = [ModuleInLine]
```

## Using fixtures to provide initial data for models
```shell
    python manage.py createsuperuser
    python manage.py runserver
```
> python manage.py dumpdata courses --indent=2

```shell
    mkdir courses/fixtures
    python manage.py dumpdata courses --indent=2 --output=courses/fixtures/subjects.json
```

> python manage.py loaddata subjects.json

## Creating models for polymorphic content

> Edit the models.py file of the courses app

```python
    from django.contrib.contenttypes.fields import GenericForeignKey
    from django.contrib.contenttypes.models import ContentType

    class Conten(models.Model):
        module = models.ForeignKey(
            Module,
            related_name='contents',
            on_delete=models.CASCADE
        )
        content_type = models.ForeignKey(
            ContentType,
            on_delete=models.CASCADE
        )
        object_id = models.PositiveIntegerField()
        item = GenericForeignKey('content_type', 'object_id')
```

## Using model inheritance
> You can read more about class inheritance at https://docs.python.org/3/tutorial/classes.html#inheritance

> Django offers the following three options to use model inheritance:
> - Abstract models: Useful when you want to put some common information into several models
> - Multi-table model inheritance: Applicable when each model in the hierarchy is considered a complete model by itself
> - Proxy models: Useful when you need to change the behavior of a model, for example, by including additional methods, changing the default manager, or using different meta options Let’s take a closer look at each of them.
  - ### **Abstract models**
    > An abstract model is a base class in which you define the fields you want to include in all child models. Django doesn’t create any database tables for abstract models. A database table is created for each child model, including the fields inherited from the abstract class and the ones defined in the child model.

    > To mark a model as abstract, you need to include abstract=True in its Meta class. Django will recognize that it is an abstract model and will not create a database table for it. To create child models, you just need to subclass the abstract model.

    ```python
    from django.db import models

    class BaseContent(models.Model):
        title = models.CharField(max_length=100)
        created = models.DateTimeField(auto_now_add=True)
        class Meta:
            abstract = True

    class Text(BaseContent):
        body = models.TextField()
    ```
    > In this case, Django would create a table for the Text model only, including the title, created, and body fields.
  - ### **Multi-table model inheritance**
    > In multi-table inheritance, each model corresponds to a database table. Django creates a OneToOneField field for the relationship between the child model and its parent model. To use multi-table inheritance, you have to subclass an existing model. Django will create a database table for both the original model and the sub-model.
    ```python
      from django.db import models

      class BaseContent(models.Model):
          title = models.CharField(max_length=100)
          created = models.DateTimeField(auto_now_add=True)

      class Text(BaseContent):
          body = models.TextField()
    ```
    > Django will include an automatically generated OneToOneField field in the Text model that points to the BaseContent model. The name for this field is basecontent_ptr, where ptr stands for pointer. A database table is created for each model.

  - ### **Proxy models**
    > A proxy model changes the behavior of a model. Both models operate on the database table of the original model. This allows you to customize behavior for different models without creating a new database table, creating different versions of the same model that are tailored for different purposes. To create a proxy model, add proxy=True to the Meta class of the model.
    ```python
        from django.db import models
        from django.utils import timezone

        class BaseContent(models.Model):
            title = models.CharField(max_length=100)
            created = models.DateTimeField(auto_now_add=True)

        class OrderedContent(BaseContent):
            class Meta:
                proxy = True
                ordering = ['created']
            def created_delta(self):
                return timezone.now() - self.created
    ```
    > Here, you define an OrderedContent model that is a proxy model for the Content model. This model provides a default ordering for QuerySets and an additional created_delta() method. Both models, Content and OrderedContent, operate on the same database table, and objects are accessible via the ORM through either model

## Creating the Content models

```python 
    class ItemBase(models.Model):
        owner = models.ForeignKey(
            User,
            related_name='%(class)s_related',
            on_delete=models.CASCADE
        )
        title = models.CharField(max_length=250)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)

        class Meta:
            abstract = True
        
        def __str__(self):
            return self.title

    class Text(ItemBase):
        content = models.TextField()

    class File(ItemBase):
        file = models.FileField(upload_to='files')

    class Image(ItemBase):
        file = models.ImageField(upload_to='images')

    class Video(ItemBase):
        url = models.URLField()
```

> Edit the Content model
```python 
    content_type = models.ForeignKey(
            ContentType,
            on_delete=models.CASCADE,
            limit_choices_to={
                'model__in':('text', 'video', 'image', 'file')
            }
    )
```
> python manage.py makemigrations

> python manage.py migrate

## Creating custom model fields
> Create a new fields.py file inside the courses app dir
```python
    from django.core.exceptions import ObjectsDoesNotExist
    from django.db import models

    class OrderField(models.PositiveIntegerFields):
        def __init__(self, for_fields=None, *args, **kwargs):
            self.for_fields = for_fields
            super().__init__(*args, **kwargs)
        def pre_save(self, model_instance, add):
            if getattr(model_instance, self.attname) is None:
                # no current value
                try:
                    qs = self.model.objects.all()
                    if self.for_fields:
                        # filter by objects with the same field values
                        # for the fields in "for_fields"
                        query = {
                            field: getattr(model_instance, field)
                            for field in self.for_fields
                        }
                        qs = qs.filter(**query)
                    # get the order of the last item
                    last_item = qs.latest(self.attname)
                    value = getattr(last_item, self.attrname) + 1
                except ObjectsDoesNotExist:
                    value = 0
                setattr(model_instance, self.attname, value)
                return value
            else:
                return super().pre_save(model_instance, add)
```

## Adding ordering to Module and Content objects
> Edit the models.py file on the courses app
```python
    from .fields import OrderField

    class Module(models.Model):
        # ...
        order = OrderField(blank=True, for_fields=['course'])

        class Meta:
            ordering = ['order']

        def __str__(self):
            return f'{self.order}. {self.title}'

    class Content(models.Model):
        # ...
        order = OrderField(blank=True, for_fields=['module'])

        class Meta:
            ordering = ['order']
```
> python manage.py makemigrations courses

```
It is impossible to add a non-nullable field 'order' to content without specifying a default. This is because the database needs something to populate existing rows. 
Please select a fix:
  1) Provide a one-off default now (will be set on all existing rows with a null
value for this column)
  2) Quit and manually define a default value in models.py.
Select an option:```
```
> Enter 1 and press Enter
```
Please enter the default value as valid Python.
The datetime and django.utils.timezone modules are available, so it is possible
to provide e.g. timezone.now as a value.
Type 'exit' to exit this prompt
>>>
```
> Enter 0 so that this is the default value for existing records and press Enter.

> Django will ask you for a default value for the Module model, too. Choose the first(1) option and enter 0 as the default value again.

> python manage.py migrate

> python manage.py shell

```
>>> from django.contrib.auth.models import User
>>> from courses.models import Subject, Course, Module
>>> user = User.objects.last()
>>> subject = Subject.objects.last()
>>> c1 = Course.objects.create(subject=subject, owner=user, title='Course 1',
slug='course1')

>>> m1 = Module.objects.create(course=c1, title='Module 1')
>>> m1.order
0

>>> m2 = Module.objects.create(course=c1, title='Module 2')
>>> m2.order
1

>>> m3 = Module.objects.create(course=c1, title='Module 3', order=5)
>>> m3.order
5

>>> m4 = Module.objects.create(course=c1, title='Module 4')
>>> m4.order
6

>>> c2 = Course.objects.create(subject=subject, title='Course 2',
slug='course2', owner=user)
>>> m5 = Module.objects.create(course=c2, title='Module 1')
>>> m5.order
0
```

## Adding authentication views
> Adding an authentication system

> Edit the main urls.py file of the educa project
```python
    from django.conf import settings
    from django.conf.urls.static
    from django.contrib import admin
    from django.contrib.auth import views as auth_views
    from django.urls import path

    urlpatterns = [
        path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
        path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
        path('admin/', admin.site.urls),
    ]

    if settings.DEBUG:
        urlpatterns += static(
            setting.MEDIA_URL, document_root=settings.MEDIA_ROOT
        )
```
## Creating the authentication templates
> Create the following file structure inside the courses application directory:
```
    templates/
        base.html
        registration/
            login.html
            logged_out.html
```
> Edit the base.html
```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>{% block title %}Educa{% endblock %}</title>
    <link href="{% static "css/base.css" %}" rel="stylesheet">
  </head>
  <body>
    <div id="header">
        <a href="/" class="logo">Educa</a>
        <ul class="menu">
          {% if request.user.is_authenticated %}
            <li>
              <form action="{% url "logout" %}" method="post">
                <button type="submit">Sign out</button>
              </form>
            </li>
          {% else %}
            <li><a href="{% url "login" %}">Sign in</a></li>
          {% endif %}
        </ul>
    </div>
    <div id="content">
      {% block content %}
      {% endblock %}
    </div>
    <script>
      document.addEventListener('DOMContentLoaded', (event) => {
        // DOM loaded
        {% block domready %}
        {% endblock %}
      })
    </script>
  </body>
</html>
```
> Edit the registration/login.html
```html
{% extends "base.html" %}

{% block title %}Log-in{% endblock %}

{% block content %}
<h1>Log-in</h1>
<div class="module">
    {% if form.errors %}
        <p>Your username and password didn't match. Please try again.</p>
    {% else %}
        <p>Please, user the following form to log-in:</p>
    {% endif %}
    <div class="login-form">
        <form action="{% url "login" %}" method="post">
            {{ form.as_p }}
            {% csrf_token %}
            <input type="hidden" name="next" value="{{ next }}">
            <p><input type="submit" value="Log-in"></p>
        </form>
    </div>
</div>
{% endblock %}
```
> Edit the registration/logged_out.html
```html
{% extends "base.html" %}

{% block title %}Logged out{% endblock %}

{% block content %}
<h1>Logged out</h1>
<div class="module">
    <p>
        You have been successfully logged out.
        You can <a href="{% url "login" %}">log-in again</a>.
    </p>
</div>
{% endblock %}
```