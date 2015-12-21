from django.conf.urls import url

from polling.views import QuestionaireCreateView, QuestionaireListView, QuestionCreateView

urlpatterns = [
    url(r'^canvassing/questionaires/add_question/', QuestionCreateView.as_view(), name='question_create'),
    url(r'^canvassing/questionaires/create/', QuestionaireCreateView.as_view(), name='questionaire_create'),
    url(r'^canvassing/questionaires/', QuestionaireListView.as_view(), name='questionaire_list'),
]
