from django.db import models
from django.urls import reverse


# class Answer(models.Model):
#     title = models.CharField(max_length=250)


# class Question(models.Model):
#     name = models.TextField()
    
#     class Status(models.TextChoices):
#         ONE = "ONE","One answer"
#         MANY = "MANY", "Several answer"

#     def __str__(self) -> str:
#         return self.body


class Questionnaire(models.Model):
    """ Модель анкеты пользователя """
    title = models.CharField(max_length=100)
    description = models.TextField()
    question_list = [
        {1: "Ответ 1"},
        {2: "Ответ 2"},
        {3: "Ответ 3"},
        {4: "Ответ 4"},
    ]
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="questions")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("polls:questionnaire_detail", args=[self.pk])


class Polls(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    # question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="polls")


