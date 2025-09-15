from django.shortcuts import render

from .models import Questionnaire

def questionnaire_list(request):
    """ Выводит на экран список Анкет """
    questionnaires = Questionnaire.objects.all()
    return render(request, 'polls/questionnaire/list.html', {"questionnaires":questionnaires})

def questionnaire_detail(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    return render(request, 'polls/questionnaire/detail.html', {'questionnaire': questionnaire})