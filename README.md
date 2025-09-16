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

[2. Enhancing Your Blog and Adding Social Features](#2-enhancing-your-blog-and-adding-social-features)

- [Using canonical URLs for models](#using-canonical-urls-for-models)
- [Creating SEO-friendly URLs for posts](#creating-seo-friendly-urls-for-posts)
- [Adding pagination to the post list view](#adding-pagination-to-the-post-list-view)
- [Building class-based views](#building-class-based-views)
- [Sending emails with Django](#sending-emails-with-django)
- [Using Django forms to share posts via email](#using-django-forms-to-share-posts-via-email)
- [Adding comments to posts using forms from models](#adding-comments-to-posts-using-forms-from-models)

  #### back chapter02

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
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{% block title %}{% endblock %}</title>
        <link rel="stylesheet" href="{% static "css/blog.css" %}">
      </head>
      <body>
        <div id="content">
          {% block content %} {% endblock %}
          <div id="sidebar">
            <h2>My blog</h2>
            <p>This is my blog.</p>
          </div>
        </div>
      </body>
    </html>
    ```

  - #### Creating the post list template

    ```html
    {% extends "blog/base.html" %}

    {% block title %}My Blog{% endblock %}

    {% block content%}
    <h1>My Blog</h1>
    {% for post in posts %}
    <h2>
      <a hrer="{% url "blog:post_detail" post.id %}">
        {{ post.title }}
      </a>
    </h2>
    <p class="date">
      Published {{ post.publish }} by {{ post.author }}
    </p>
    {{ post.body|truncatewords:30|linebreaks }}
    {% endfor %}
    {% endblock %}
    ```

    - #### Creating the post detail template

      ```html
      {% extends "blog/base.html" %} {% block title %}{{ post.title}}{% endblock
      %} {% block content %}
      <h1>{{ post.title }}</h1>
      <p class="date">Published {{ post.publish }} by {{ post.author }}</p>
      {{ post.body|linebreaks }} {% endblock %}
      ```

    ```

    ```

- ### Understanding the Django request/response cycle
  1. HttpRequest ->
  2. URL PATTERNS: path('blog/< id >/', post_detail),
  3. -> VIEWS: post_detail
  4. -> DATABASE: SELECT\*FROM POSTS ID = 3
     <- 3, "One more post", "Post body."
  5. render Html template

# 2. Enhancing Your Blog and Adding Social Features

- #### Using canonical URLs for models

  ```python
      from django.conf import settings
      from django.db import models
      from django.urls import reverse
      from django.utils import timezone

      class PublishedManager(models.Manager):
          def get_queryset(self):
            return super().get_queryset().filter(status=Post.Status.PUBLISHED)

      class Post(models.Model):
          # ...

          def __str__(self):
              return self.title

          def get_absolute_url(self):
              return reverse('blog:detail', args=[self.id])
  ```

- ### Creating SEO-friendly URLs for posts
    ```python
        class Post(models.Model):
          # ...
          slug = models.SlugField(
              max_length=250,
              unique_for_date='publish',
          )
          # ...
    ```
    - #### Modifying the URL patterns
      ```python 
      path(
          '<int:year>/<int:month>/<int:day>/<slug:post>/,
          views.post_detail,
          name=post_detail
      )
    - #### Modifying the views
      ```python
        def post_detail(request, year, month, day, post):
            post = get_object_or_404(
                Post,
                status=Post.Status.PUBLISHED,
                publish__year=year,
                publish__month=month,
                publish__day=day
            )
            return render(request, 'blog/post/detail.html', {"post": post})
      ```
      - #### Modifying the canonical URL for posts
      ```python
        class Post(models.Model):
            # ...
            def get_absolute_url(): 
                return reverse(
                    'blog:post_detail',
                    args = [
                        self.publish.year,
                        self.publish.month,
                        self.publish.day,
                        self.slug
                    ]

                )
      ```
- ### Adding pagination to the post list view
    ```python
        from django.core.paginator import Paginator
        from django.shortcuts import get_object_or_404, render
        from .models import Post


        def post_list(request):
            post_list = Post.objects.all()
            # Pagination with 3 posts per page
            pagination = Paginator(post_list, 3)
            page_number = request.GET.get('page', 1)
            posts = paginator.page(page_number)

            return render(
                request, 
                'blog/post/list.html,
                {"posts":"posts"}
            )
    ```
    - #### Creating a pagination template
      > templates/pagination.html
      ```html
        <div class="pagination">
          <span class="step-links">
          {% if page.has_previous %}
            <a href="?page={{ page.previous_page_number }}">Previous</a>
          {% endif %}
          <span class="current">
            Page {{ page.number }} of {{ page.paginator.num_pages }}.
          </span>
          {% if page.has_next %}
            <a href="?page={{ page.next_page_number }}">Next</a>
          {% endif %}
          </span>
        </div>
      ```
      > blog/post/list.html
      ```html
          # ...
          {% include "pagination.html" with page=posts %}
          {% endblock %}
      ```
    - #### Handling pagination errors
      ```python
          from django.shortcuts import get_object_or_404, render
          from .models import Post
          from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

          def post_list(request):
              post_list = Post.published.all()
              # Pagination with 3 posts per page
              paginator = Paginator(post_list, 3)
              page_number = request.GET.get('page')
              try:
                  posts = paginator.page(page_number)
              except PageNotAnInteger:
                  # If page_number is not an integer get the first page
                  posts = paginator.page(1)
              except EmptyPage:
                  # If page_number is out of range get last page of results
                  posts = paginator.page(paginator.num_pages)
              return render(
                  request,
                  'blog/post/list.html',
                  {'posts': posts}
              )
          ```
- ### Building class-based views
    - #### Using a class-based view to list posts
        ```python
          from django.views.generic import ListView

          class PostListView(ListView):
              """ 
              Alternative post list view
              """
              queryset = Post.published.all()
              context_object_name = 'posts'
              paginate_by = 3
              template_name = 'blog/post/list.html'
        ```
        > blog/urls.py

        ```python
          path('', views.PostListView.as_view(), name='post_list'),
        ```
        > blog/post/list.html
        ```html
          {% include "pagination.html" with page=page_obj %}
          {% endblock %}
        ```

- ### Sending emails with Django
    - #### Creating forms with Django
      ```python
          from django import forms

          class EmailPostForm(forms.Form):
              name = forms.CharField(max_length=25)
              email = forms.EmailField()
              to = forms.EmailField()
              comments = forms.CharField(
                  require=False,
                  widget=forms.Textarea
              )
      ```
    - #### Handling forms in views
      ```python
        from .forms import EmailPostForm

        def post_share(request, post_id):
            # Retrieve post by id
            post = get_object_or_404(
                Post,
                id=post_id,
                status=Post.Status.PUBLISHED
            )
            if request.method == 'POST':
                # Form was submitted
                form = EmailPostForm(request.POST)
                if form.is_valid():
                # Form fields passed validation
                cd = form.cleaned_data
                # ... send email
            else:
                form = EmailPostForm()
            return render(
                request,
                'blog/post/share.html',
                {
                    'post': post,
                    'form': form
                }
            )
      ```
    - #### Working with environment variables
        ```shell
          python -m pip install python-decouple==3.8
        ```
        > Create a new file inside your project's root directory and name it .env.
        ```python
          EMAIL_HOST_USER=your_account@gmail.com
          EMAIL_HOST_PASSWORD=
          DEFAULT_FROM_EMAIL=My Blog <your_account@gmail.com>
        ```
        > Edit the settings.py file of your project and add the following code to it:

        ```python
          from decouple import config
          # ...
          # Email server configuration
          EMAIL_HOST = 'smtp.gmail.com'
          EMAIL_HOST_USER = config('EMAIL_HOST_USER')
          EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
          EMAIL_PORT = 587
          EMAIL_USE_TLS = True
          DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
        ```
      
      > console \
      > EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'\
      > smtp\
      > EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
      ```shell
          python manage.py shell

          >>> from django.core.mail import send_mail
          >>> send_mail('Django mail',
          ...        'This e-mail was sent with Django.',
          ...        'your_account@gmail.com',
          ...        ['your_account@gmail.com'],
          ...        fail_silently=False)
      ```
    - #### Sending emails in views
      ```python
          # ...
          from django.core.mail import send_mail
          # ...
          def post_share(request, post_id):
              # Retrieve post by id
              post = get_object_or_404(
                    Post,
                    id=post_id,
                    status=Post.Status.PUBLISHED
              )
              sent = False
              if request.method == 'POST':
                  # Form was submitted
                  form = EmailPostForm(request.POST)
                  if form.is_valid():
                  # Form fields passed validationChapter 2
                  cd = form.cleaned_data
                  post_url = request.build_absolute_uri(
                        post.get_absolute_url()
                  )
                  subject = (
                      f"{cd['name']} ({cd['email']}) "
                      f"recommends you read {post.title}"
                  )
                  message = (
                      f"Read {post.title} at {post_url}\n\n"
                      f"{cd['name']}\'s comments: {cd['comments']}"
                  )
                  send_mail(
                      subject=subject,
                      message=message,
                      from_email=None,
                      recipient_list=[cd['to']]
                  )
                  sent = True
              else:
                  form = EmailPostForm()
              return render(
                  request,
                  'blog/post/share.html',
                  {
                      'post': post,
                      'form': form,
                      'sent': sent
                  }
              )
        # Adding blog/urls.py
        path('<int:post_id>/share/', views.post_share, name='post_share'),
      ```
    - #### Rendering forms in templates
      > blog/templates/blog/post/
      ```html
      {% extends "blog/base.html" %}

      {% block title %}Share a post{% endblock %}
      {% block content %}
        {% if sent %}
        <h1>E-mail successfully sent</h1>
        <p>
          "{{ post.title }}" was successfully sent to {{ form.cleaned_data.to }}.
        </p>
        {% else %}
          <h1>Share "{{ post.title }}" by e-mail</h1>
          <form method="post">
            {{ form.as_p }}
            {% csrf_token %}
            <input type="submit" value="Send e-mail">
          </form>
        {% endif %}
      {% endblock %}
      ```
      > blog/post/detail.html
      ```html
        {% extends "blog/base.html" %}
        {% block title %}{{ post.title }}{% endblock %}
        {% block content %}
          <h1>{{ post.title }}</h1>
          <p class="date">
            Published {{ post.publish }} by {{ post.author }}
            </p>
              {{ post.body|linebreaks }}
            <p>
              <a href="{% url "blog:post_share" post.id %}">
                Share this post
              </a>
            </p>
        {% endblock %}
      ```

- ### Adding comments to posts using forms from models

  - #### Creating a comment system

    - Creating a model for comments

      ```python
        class Comment(models.Model):
            post = models.ForeignKey(
                Post,
                on_delete=models.CASCADE,
                related_name='comments'
            )
            name = models.CharField(max_length=80)
            email = models.EmailField()
            body = models.TextField()
            created = models.DateTimeField(auto_now_add=True)
            updated = models.DateTimeField(auto_now=True)
            active = models.BooleanField(default=True)

            class Meta:
                ordering = ['created']
                indexes = [
                    models.Index(fields=['created']),
                ]
            def __str__(self):
                return f"Comment by {self.name} on {self.post}"
      ```

      ```shell
        python manage.py makemigrations blog
          Migrations for 'blog':
            blog/migrations/0003_comment.py
              - Create model Comment
        python manage.py migrate
      ```

    - Adding comments to the administration site

      ```python
        from .models import Comment, Post

        @admin.register(Comment)
        class CommentAdmin(admin.ModelAdmin):
            list_display = ['name', 'email', 'post', 'created', 'active']
            list_filter = ['name', 'email', 'updated']
            search_fields = ['name', 'email', 'body']
      ```

    - Creation forms from models

      ```python
          from .models import Comment

          class CommentForm(forms.ModelForm):
              class Meta:
                  fields = ['name', 'email', 'body']
      ```

    - Handling ModelForm in views

      ```python
          from django.core.mail import send_mail
          from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
          from django.shortcuts import get_object_or_404, render
          from django.views.decorators.http import require_POST
          from django.views.generic import ListView
          from .forms import CommentForm, EmailPostForm
          from .models import Post

          # ...

          @require_POST
          def post_comment(request, post_id):
              post = get_object_or_404(
                  Post,
                  id=post_id,
                  status=Post.Status.PUBLISHED
              )
              comment = None
              form = CommentForm(data=request.POST)
              if form.is_valid():
                  comment = form.save(commit=False)
                  comment.post = post
                  comment.save()
              return render(
                  request, 'blog/post/comment.html',
                  {"post":post, "form":form, "comment": comment}
              )
      ```

      ```python
          urlpatterns = [
              # ...
              path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
          ]
      ```

    - Creating templates for the comment form
      > blog/post/includes/comment_form.html
      ```html
        <h2>Add a new comment</h2>
        <form action="{% url "blog:post_comment" post.id %}" method="post">
          {{ form.as_p }}
          {% csrf_token %}
          <p><input type="submit" value="Add comment"></p>
        </form>
      ```
      > blog/post/comment.html
      ```html
      {% extends "blog/base.html" %} {% block title %}Add a comment{% endblock
      %} {% block content %} {% if comment %}
      <h2>Your comment has been added.</h2>
      <p><a href="{{ post.get_absolute_url }}">Back to the post</a></p>
      {% else %} {% include "blog/post/includes/comment_form.html" %} {% endif
      %} {% endblock %}
      ```
    - Adding comments to the post detail view
      ```python
        def post_detail(request, year, month, day, post):
            post = get_object_or_404(
                Post,
                status=Post.Status.PUBlISHED,
                publish__year=year,
                publish__month=month,
                publish__day=day
            )
            # list of active comments for this post
            comment = post.comment.filter(active=True)
            # form for users to comment
            form = CommentForm()
            return render(
                request,
                'blog/post/detail.html',
                {
                    'post': post,
                    'comments': comments,
                    'form': form
                }
            )
      ```
    - Adding comments to the post detail template
      ```html
          {% extends "blog/base.html" %}
          {% block title %}{{ post.title }}{% endblock %}
          {% block content %}
            <h1>{{ post.title }}</h1>
            <p class="date">
              Published {{ post.publish }} by {{ post.author }}
            </p>
          {{ post.body|linebreaks }}
          <p>
          <a href="{% url "blog:post_share" post.id %}">
            Share this post
          </a>
          </p>
          {% with comments.count as total_comments %}
            <h2>
              {{ total_comments }} comment{{ total_comments|pluralize }}
            </h2>
          {% endwith %}
          {% endblock %}
      ```
      ```html
      {% endwith %}
      {% for comment in comments %}
        <div class="comment">
          <p class="info">
            Comment {{ forloop.counter }} by {{ comment.name }}
            {{ comment.created }}
          </p>
          {{ comment.body|linebreaks }}
        </div>
      {% empty %}
        <p>There are no comments.</p>
      {% endfor %}
      {% include "blog/post/includes/comment_form.html" %}
      {% endblock %}
      ```
    - Using simplified templates for form rendering
      ```html
        {% for field in form %}
          <div class="my-div">
            {{ field.errors }}
            {{ field.label_tag }} {{ field }}
            <div class="help-text">{{ field.help_text|safe }}</div>
          </div>
        {% endfor %}
      ```
      > blog/post/includes/comment_form.html
      ```html
        <h2>Add a new comment</h2>
        <form action="{% url "blog:post_comment" post.id %}" method="post">
          <div class="left">
            {{ form.name.as_field_group }}
          </div>
          <div class="left">
            {{ form.email.as_field_group }}
          </div>
          {{ form.body.as_field_group }}
          {% csrf_token %}
          <p><input type="submit" value="Add comment"></p>
        </form>
      ```
[back chapter02](#back-chapter02)
