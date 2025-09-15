from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("polls:questionnaire_detail", args=[self.pk])
    

# class Polls(models.Model):
#     # question
#     # answer
#     pass

# class Question(models.Model):
#     # title
#     # textfield
#     # answer_option
#     pass

# class Answer(models.Model):
#     #text choice
#     pass
