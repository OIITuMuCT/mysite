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
    - [Creating model managers](#creating-model-managers)
- [Building views, templates, and URLs](#building-views-templates-and-urls)
    - [Creating list and detail views](#creating-list-and-detail-views)
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
    ```shell
      >>> post.title = 'New title'
      >>> post.save()
    ```

  - Retrieving objects
    ```shell
    >>> all_posts = Post.objects.all()
    
    >>> Post.objects.all()
    <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>
    ```
  - Filtering objects
    ```shell
        >>> Post.objects.filter(title="Who was Django Reinhardt?")
        >>> print(posts.query)
        SELECT  "blog_post"."id", "blog_post"."title", "blog_post"."slug",
                "blog_post"."body", "blog_post"."publish", "blog_post"."created", 
                "blog_post"."updated", "blog_post"."status", "blog_post"."author_id" 
        FROM "blog_post" WHERE "blog_post"."title" = Who was Django Reinhardt? ORDER BY "blog_post"."publish" DESC
    ```
  - Using field lookups
    ```shell
      >>> Post.objects.filter(id__exact=1)
      <QuerySet [<Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(title__exact='who was django reinhardt?')
      <QuerySet []>

      >>> Post.objects.filter(title__contains='Django')
      <QuerySet [<Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(id__in=[1, 3])
      <QuerySet [<Post: One more post>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(id__in=[1, 2, 3])
      <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(id__gt=3)
      <QuerySet []>

      >>> Post.objects.filter(id__gte=3)
      <QuerySet [<Post: One more post>]>

      >>> Post.objects.filter(id__lt=3)
      <QuerySet [<Post: New title>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(id__lte=3)
      <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(publish__date=date(2025, 9, 12))
      <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.filter(author__username='admin')
      <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>
    ```
  - Chaining filters
    ```shell 
      Post.objects.filter(publish__year=2025) \
                  .filter(author__username='admin')
      <QuerySet [<Post: One more post>, <Post: New title>, <Post: Who was Django Reinhardt?>]>

      >>> Post.objects.order_by('author', 'title')
      <QuerySet [<Post: New title>, <Post: One more post>, <Post: Who was Django Reinhardt?>, <Post: New post user2>]
    ```

  - Ordering objects
      ```shell
      >>> Post.objects.order_by('author', 'title')

      <QuerySet [<Post: New title>, <Post: One more post>, <Post: Who was Django Reinhardt?>, <Post: New post user2>]
      ```
  - Limiting QuerySets
    
    ```shell
      >>> Post.objects.all()[:3]
      <QuerySet [<Post: New post user2>, <Post: One more post>, <Post: New title>]>
    ```
  - Deleting objects
    ```shell
      >>> post = Post.objects.get(id=2)
      post.delete()
    ```
  - Complex lookups with Q objects
    ```shell
      >>> starts_who = Q(title__istartswith='who')
      >>> starts_one = Q(title__istartswith='one')
      >>> Post.objects.filter(starts_who | starts_one)
      >>> <QuerySet [<Post: One more post>, <Post: Who was Django Reinhardt?>]>
    ```
  - More on QuerySets
    > https://docs.djangoproject.com/en/5.0/ref/models/querysets/

  - #### Creating model managers
    ```python
    class PublishedManager(models.Manager):
        def get_queryset(self):
            return (
              super().get_queryset().filter(status=Post.Status.PUBLISHED)
            )
    class Post(models.Model):
      # models fields
      # ...
      objects = models.Manager() # The default manager.
      published = PublishedManager() # custom manager.
      # ...
    ```
- ### Building views, templates, and URLs
  - #### Creating list and detail views
    ```python
      from django.shortcuts import render
      from .models import Post

      def post_list(request):
          posts = Post.published.all()
          return render(request, 'blog/post/list.html', {'posts': posts})

      def post_detail(request, id):
          try:
              post = Post.published.get(id=id)
          except Post.DoesNotExist:
              raise Http404("No Post found.")
          return render(request, 'blog/post/detail.html', {"post": post})
    ```
  - #### Adding URL patterns for your views
    ```python
    # blog/urls.py
      from django.urls import path
      from . import views

      app_name = 'blog'

      urlpatterns = [
      # post views
          path('', views.post_list, name='post_list'),
          path('<int:id>/', views.post_detail, name='post_detail'),
      ]
      # mysite/urls.py

      from django.contrib import admin
      from django.urls import include, path

      urlpatterns = [
          path('admin/', admin.site.urls),
          path('blog/', include('blog.urls', namespace='blog')),
      ]
    ```
  - #### Creating templates for your views
    ```shell
    templates/
        blog/
            base.html
            post/
                list.html
                detail.html
    ```
  - #### Creating a base template
    This text will be <mark>highlighted</mark>.
    
    ```html
      {% load static %}
      <!DOCTYPE html>
      <html lang="en">
      <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title> {% block title %}{% endblock %} </title>
          <link rel="stylesheet" href="{% static "css/blog.css" %}">
      </head>
      <body>
          <div id="content">
              {% block content %}
              {% endblock %}
              <div id="sidebar">
                  <h2>My blog</h2>
                  <p>This is my blog.</p>
              </div>
          </div>
      </body>
      </html>
    ```
- ### Understanding the Django request/response cycle
