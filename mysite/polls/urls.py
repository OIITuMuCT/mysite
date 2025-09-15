from django.urls import path
from . import views


app_name = "polls"

urlpatterns = [
    # path("", views.questionnaire_list, name="questionnaire_list"),
    path("", views.QuestionnaireListView.as_view(), name="questionnaire_list"),
    path("<int:id>/", views.questionnaire_detail, name='questionnaire_detail'),
    path("<int:id>/share/", views.questionnaire_share, name='questionnaire_share'),
]
