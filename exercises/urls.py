from django.urls import path
from . import views

app_name = 'exercises'

urlpatterns = [
    path('', views.exercise_list, name='exercise_list'),
    path('<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
    path('dyslexia/<int:attempt_id>/', views.dyslexia_exercise, name='dyslexia_exercise'),
    path('dyscalculia/<int:attempt_id>/', views.dyscalculia_exercise, name='dyscalculia_exercise'),
    path('attempt/<int:attempt_id>/question/<int:question_index>/', views.get_question, name='get_question'),
    path('attempt/<int:attempt_id>/submit/', views.submit_answer, name='submit_answer'),
    path('result/<int:attempt_id>/', views.exercise_result, name='exercise_result'),
]
