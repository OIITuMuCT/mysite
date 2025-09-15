from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from .models import Questionnaire
from .forms import EmailQuestionnaireForm


class QuestionnaireListView(ListView):
    queryset = Questionnaire.objects.all()
    context_object_name = 'questionnaires'
    paginate_by = 2
    template_name = 'polls/questionnaire/list.html'

def questionnaire_list(request):
    """ Выводит на экран список Анкет """
    questionnaires = Questionnaire.objects.all()
    return render(request, 'polls/questionnaire/list.html', {"questionnaires":questionnaires})

def questionnaire_detail(request, id):
    questionnaire = Questionnaire.objects.get(id=id)
    return render(request, 'polls/questionnaire/detail.html', {'questionnaire': questionnaire})


def questionnaire_share(request, id):
    # Retrieve questionnaire by id
    questionnaire = get_object_or_404(
        Questionnaire,
        id=id,
    )
    sent = False
    
    if request.method == "POST":
        # form was submitted
        form = EmailQuestionnaireForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # ... send email
            questionnaire_url = request.build_absolute_uri(
                questionnaire.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']})"
                f"recommends you see {questionnaire.title}"
            )
            message = (
                f"Read {questionnaire.title} at {questionnaire_url}\n\n"
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
        form = EmailQuestionnaireForm()
    return render(
        request,
            'polls/questionnaire/share.html',
            {
                "questionnaire": questionnaire, 
                "form": form,
                "sent": sent
            }
        )