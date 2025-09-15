from django.db import models




class Questionnaire(models.Model):
    """ Модель анкеты пользователя """
    title = models.CharField(max_length=100)
    description = models.TextField()
    # question_list = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
