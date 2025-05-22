# from django.urls import path
# from . import views

# app_name = 'accounts'

# urlpatterns = [
#     path('profile/', views.profile_view, name='profile'),
#     path('toggle-dyslexia-mode/', views.toggle_dyslexia_mode, name='toggle_dyslexia_mode'),
#     path('children/', views.children_list, name='children_list'),
#     path('children/add/', views.add_child, name='add_child'),
#     path('children/<int:child_id>/edit/', views.edit_child, name='edit_child'),
#     path('students/', views.students_list, name='students_list'),
#     path('students/add/', views.add_student, name='add_student'),
#     path('students/<int:student_id>/remove/', views.remove_student, name='remove_student'),

# ]

# from django.urls import path
# from . import views

# app_name = 'accounts'

# urlpatterns = [
#     path('profile/', views.profile_view, name='profile'),
#     path('toggle-dyslexia-mode/', views.toggle_dyslexia_mode, name='toggle_dyslexia_mode'),
#     path('children/', views.children_list, name='children_list'),
#     path('children/add/', views.add_child, name='add_child'),
#     path('children/<int:child_id>/edit/', views.edit_child, name='edit_child'),
#     path('children/<int:child_id>/delete/', views.delete_child, name='delete_child'),
#     path('students/', views.students_list, name='students_list'),
#     path('students/add/', views.add_student, name='add_student'),
#     path('students/<int:student_id>/remove/', views.remove_student, name='remove_student'),
# ]

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('toggle-dyslexia-mode/', views.toggle_dyslexia_mode, name='toggle_dyslexia_mode'),
    path('children/', views.children_list, name='children_list'),
    path('children/add/', views.add_child, name='add_child'),
    path('children/<int:child_id>/edit/', views.edit_child, name='edit_child'),
    path('children/<int:child_id>/delete/', views.delete_child, name='delete_child'),
    path('students/', views.students_list, name='students_list'),
    path('students/add/', views.add_student, name='add_student'),
    path('students/<int:student_id>/remove/', views.remove_student, name='remove_student'),
]