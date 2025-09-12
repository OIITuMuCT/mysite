[1. Building a Blog Application ](#1-building-a-blog-application)

- [Installing Python](#installing-python)
- [Creating a Python virtual environment](#creating-a-python-virtual-environment)
- [Installing Django](#installing-django)
- [Creating and configuring a Django project](#creating-and-configuring-a-django-project)
- [Building a Django application](#building-a-django-application)
- [Designing data models](#designing-data-models)
    - [Creating the Post model](#creating-the-post-model)
- [Creating and applying model migrations](#creating-and-applying-model-migrations)
- [Setting up an administration site for your models](#setting-up-an-administration-site-for-your-models)
- [Working with QuerySets and model managers](#working-with-querysets-and-model-managers)
- [Building views, templates, and URLs](#building-views-templates-and-urls)
- [Understanding the Django request/response cycle](#understanding-the-django-requestresponse-cycle)

# 1. Building a Blog Application

- ### Installing Python
  ```shell
      python --version
      python 3.12.4
  ```
- ### Creating a Python virtual environment

  ```shell
      python -m venv venv
      source venv/bin/activate
  ```

- ### Installing Django

  ```shell
      python -m pip install Django~=5.0.4
      python -m django --version
  ```

  > django documentation https://docs.djangoproject.com/en/5.2/

- ### Creating and configuring a Django project
    Creating your first project
    ```shell
    django-admin startproject mysite
    ```
    ```
    mysite/
      manage.py
      mysite/
        __init__.py
        asgi.py
        settings.py
        urls.py
        wsgi.py
    ```
    Applying initial database migrations
    ```shell
    cd mysite
    python manage.py migrate
    ```
    ```shell
    Operations to perform:
     Apply all migrations: admin, auth, contenttypes, sessions
    Running migrations:
     Applying contenttypes.0001_initial... OK
     Applying auth.0001_initial... OK
     Applying admin.0001_initial... OK
     Applying admin.0002_logentry_remove_auto_add... OK
     Applying admin.0003_logentry_add_action_flag_choices... OK
     Applying contenttypes.0002_remove_content_type_name... OK
     Applying auth.0002_alter_permission_name_max_length... OK
     Applying auth.0003_alter_user_email_max_length... OK
     Applying auth.0004_alter_user_username_opts... OK
     Applying auth.0005_alter_user_last_login_null... OK
     Applying auth.0006_require_contenttypes_0002... OK
     Applying auth.0007_alter_validators_add_error_messages... OK
     Applying auth.0008_alter_user_username_max_length... OK
     Applying auth.0009_alter_user_last_name_max_length... OK
     Applying auth.0010_alter_group_name_max_length... OK
     Applying auth.0011_update_proxy_permissions... OK
     Applying auth.0012_alter_user_first_name_max_length... OK
     Applying sessions.0001_initial... OK
    ```
    Running the development server
    ```shell
    python manage.py runserver
    ```
- ### Building a Django application
    Creating an application
    ```shell
    python manage.py startapp blog
    ```
    ```
      blog/
        migrations/
            __init__.py
        __init__.py
        admin.py
        apps.py
        models.py
        tests.py
        views.py
    ```

- ### Designing data models
    Creating the blog data models
    - #### Creating the Post model

      ```python
      from django.db import models
      from django.utils import timezone
      from django.contrib.auth.models import User


      class Post(models.Model):
          class Status(models.TextChoices):
              DRAFT = "DF", "Draft"
              PUBLISHED = "PB", "Published"

          title = models.CharField(max_length=250)
          slug = models.SlugField(max_length=250)
          body = models.TextField()
          publish = models.DateTimeField(default=timezone.now)
          created = models.DateTimeField(auto_now_add=True)
          updated = models.DateTimeField(auto_now=True)
          status = models.CharField(
              max_length=2, choices=Status.choices, default=Status.DRAFT
          )
          author = models.ForeignKey(
              User, on_delete=models.CASCADE, related_name="blog_posts"
          )

          class Meta:
              ordering = ["-publish"]
              indexes = [
                  models.Index(fields=["-publish"]),
              ]

          def __str__(self):
              return self.title

        ```
    - #### Adding a status field
      ```python
      class Post(models.Model):
          class Status(models.TextChoises):
              DRAFT = 'DF', 'Draft'
              PUBLISHED = 'PB', 'Published'
      # ...
          status = models.CharField(
            max_length=2,
            choices=Status,
            # choices=Status.choices
            default=Status.DRAFT
          )
      ```
      ```shell
      python manage.py shell
      >>> from blog.models import Post

      >>> Post.Status.choices
      [('DF', 'Draft'), ('PB', 'Published')]

      >>> Post.Status.labels
      ['Draft', 'Published']

      >>> Post.Status.values
      ['DF', 'PB']

      >>> Post.Status.names
      ['DRAFT', 'PUBLISHED']
      ```
- ### Creating and applying model migrations
    > python manage.py makemigrations blog

    > python manage.py sqlmigrate blog 0001
    > python manage.py migrate
- ### Setting up an administration site for your models
   - Creating an administration site for models

     - Creating a superuser

       ```shell
       python manage.py createsuperuser
       ```
     - Adding models to the administration site
       ```python
        from django.contrib import admin
        from .models import Post

        admin.site.register(Post)
       ```
     - Customizing how models are displayed
       ```python
          from django.contrib import admin
          from .models import Post
  
          @admin.register(Post)
          class PostAdmin(admin.ModelAdmin):
              list_display = ['title', 'slug', 'author', 'publish', 'status']
              list_filter = ['status', 'created', 'publish', 'author']
              search_fields = ['title', 'body']
              prepopulated_fields = {'slug': ('title',)}
              raw_id_fields = ['author']
              date_hierarchy = 'publish'
              ordering = ['status', 'publish']
              show_facets = admin.ShowFacets.ALWAYS
       ```

- ### Working with QuerySets and model managers
  - Creating objects
    ```shell
    >>> from django.contrib.auth.models import User
    >>> from blog.models import Post
    >>> user = User.objects.get(username='admin')
    >>> post = Post(title='Another post',
    ...             slug='another-post',
    ...             body='Post body.',
    ...             author=user)
    >>> post.save()

    >>> user, created = User.objects.get_or_create(username='user2')
    ```
  - Update objects
  - Retrieving objects
  - Filtering objects
- ### Building views, templates, and URLs
- ### Understanding the Django request/response cycle
