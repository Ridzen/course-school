from django.urls import path

from .views import QuestionnaireAPIView, QuestionnaireRetrieveAPIView


urlpatterns = [
    path('api/v1/questionnaire/', QuestionnaireAPIView.as_view()),
    path('api/v1/questionnaire/<int:pk>/', QuestionnaireRetrieveAPIView.as_view()),
]
