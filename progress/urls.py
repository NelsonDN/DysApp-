from django.urls import path
from . import views

app_name = 'progress'

urlpatterns = [
    path('', views.progress_report, name='progress_report'),
    path('children/', views.children_progress, name='children_progress'),
    path('students/', views.students_progress, name='students_progress'),
    path('child/<int:child_id>/', views.child_progress, name='child_progress'),
    path('achievements/', views.achievements, name='achievements'),
    path('rewards-shop/', views.rewards_shop, name='rewards_shop'),
    path('rewards-shop/purchase/<int:reward_id>/', views.purchase_reward, name='purchase_reward'),
    # path('student/<int:student_id>/', views.student_progress, name='student_progress'),
]
