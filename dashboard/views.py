from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Avg, Sum, Q
from datetime import timedelta

from accounts.models import ChildProfile, ParentProfile, TeacherProfile
from exercises.models import ExerciseAttempt, Exercise, ExerciseType
from progress.models import ProgressRecord, UserAchievement

from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def dashboard(request):
    """
    Affiche le tableau de bord adapté au type d'utilisateur
    """
    user = request.user
    
    if user.is_child:
        return child_dashboard(request)
    elif user.is_parent:
        return parent_dashboard(request)
    elif user.is_teacher:
        return teacher_dashboard(request)
    else:
        return admin_dashboard(request)

def child_dashboard(request):
    """
    Tableau de bord pour les enfants
    """
    user = request.user
    child_profile = getattr(user, 'child_profile', None)
    
    if not child_profile:
        return redirect('accounts:profile')
    
    # Récupérer les tentatives récentes
    recent_attempts = ExerciseAttempt.objects.filter(
        user=user,
        is_completed=True
    ).order_by('-completed_at')[:5]
    
    # Récupérer les récompenses
    achievements = UserAchievement.objects.filter(
        user=user
    ).order_by('-date_earned')[:5]
    
    # Récupérer les enregistrements de progression
    progress_records = ProgressRecord.objects.filter(
        user=user
    ).order_by('-skill_level')
    
    # Recommander des exercices
    recommended_exercises = []
    
    if child_profile.has_dyslexia:
        dyslexia_exercises = Exercise.objects.filter(
            exercise_type__disorder_type__in=['dyslexia', 'both'],
            is_active=True
        ).exclude(
            attempts__user=user,
            attempts__is_completed=True
        ).order_by('?')[:2]
        
        recommended_exercises.extend(dyslexia_exercises)
    
    if child_profile.has_dyscalculia:
        dyscalculia_exercises = Exercise.objects.filter(
            exercise_type__disorder_type__in=['dyscalculia', 'both'],
            is_active=True
        ).exclude(
            attempts__user=user,
            attempts__is_completed=True
        ).exclude(
            id__in=[e.id for e in recommended_exercises]
        ).order_by('?')[:2]
        
        recommended_exercises.extend(dyscalculia_exercises)
    
    # Si pas assez d'exercices recommandés, ajouter des exercices déjà complétés
    if len(recommended_exercises) < 4:
        additional_exercises = Exercise.objects.filter(
            is_active=True
        ).exclude(
            id__in=[e.id for e in recommended_exercises]
        ).order_by('?')[:4 - len(recommended_exercises)]
        
        recommended_exercises.extend(additional_exercises)
    
    context = {
        'child_profile': child_profile,
        'recent_attempts': recent_attempts,
        'achievements': achievements,
        'progress_records': progress_records,
        'recommended_exercises': recommended_exercises
    }
    
    return render(request, 'dashboard/child_dashboard.html', context)

def parent_dashboard(request):
    """
    Tableau de bord pour les parents
    """
    user = request.user
    parent_profile = getattr(user, 'parent_profile', None)
    
    if not parent_profile:
        return redirect('accounts:profile')
    
    # Récupérer les enfants
    children = parent_profile.children.all()
    
    # Récupérer les statistiques pour chaque enfant
    children_stats = []
    
    for child in children:
        child_profile = getattr(child, 'child_profile', None)
        
        if child_profile:
            # Récupérer les tentatives récentes
            recent_attempts = ExerciseAttempt.objects.filter(
                user=child,
                is_completed=True
            ).order_by('-completed_at')[:3]
            
            # Calculer les statistiques
            total_attempts = ExerciseAttempt.objects.filter(
                user=child,
                is_completed=True
            ).count()
            
            avg_score = ExerciseAttempt.objects.filter(
                user=child,
                is_completed=True
            ).aggregate(avg=Avg('score'))['avg'] or 0
            
            # Récupérer les enregistrements de progression
            progress_records = ProgressRecord.objects.filter(
                user=child
            ).order_by('-skill_level')[:3]
            
            # Ajouter les statistiques
            children_stats.append({
                'child': child,
                'profile': child_profile,
                'recent_attempts': recent_attempts,
                'total_attempts': total_attempts,
                'avg_score': avg_score,
                'progress_records': progress_records
            })
    
    context = {
        'parent_profile': parent_profile,
        'children_stats': children_stats
    }
    
    return render(request, 'dashboard/parent_dashboard.html', context)

def teacher_dashboard(request):
    """
    Tableau de bord pour les enseignants
    """
    user = request.user
    teacher_profile = getattr(user, 'teacher_profile', None)
    
    if not teacher_profile:
        return redirect('accounts:profile')
    
    # Récupérer les élèves
    students = teacher_profile.students.all()
    
    # Récupérer les statistiques pour chaque élève
    students_stats = []
    
    for student in students:
        student_profile = getattr(student, 'child_profile', None)
        
        if student_profile:
            # Récupérer les tentatives récentes
            recent_attempts = ExerciseAttempt.objects.filter(
                user=student,
                is_completed=True
            ).order_by('-completed_at')[:3]
            
            # Calculer les statistiques
            total_attempts = ExerciseAttempt.objects.filter(
                user=student,
                is_completed=True
            ).count()
            
            avg_score = ExerciseAttempt.objects.filter(
                user=student,
                is_completed=True
            ).aggregate(avg=Avg('score'))['avg'] or 0
            
            # Récupérer les enregistrements de progression
            progress_records = ProgressRecord.objects.filter(
                user=student
            ).order_by('-skill_level')[:3]
            
            # Ajouter les statistiques
            students_stats.append({
                'student': student,
                'profile': student_profile,
                'recent_attempts': recent_attempts,
                'total_attempts': total_attempts,
                'avg_score': avg_score,
                'progress_records': progress_records
            })
    
    # Récupérer les statistiques globales
    total_students = students.count()
    active_students = ExerciseAttempt.objects.filter(
        user__in=students,
        is_completed=True,
        completed_at__gte=timezone.now() - timedelta(days=7)
    ).values('user').distinct().count()
    
    total_attempts = ExerciseAttempt.objects.filter(
        user__in=students,
        is_completed=True
    ).count()
    
    avg_score = ExerciseAttempt.objects.filter(
        user__in=students,
        is_completed=True
    ).aggregate(avg=Avg('score'))['avg'] or 0
    
    context = {
        'teacher_profile': teacher_profile,
        'students_stats': students_stats,
        'total_students': total_students,
        'active_students': active_students,
        'total_attempts': total_attempts,
        'avg_score': avg_score
    }
    
    return render(request, 'dashboard/teacher_dashboard.html', context)

def admin_dashboard(request):
    """
    Tableau de bord pour les administrateurs
    """
    # Statistiques des utilisateurs
    total_users = User.objects.count()
    total_children = User.objects.filter(user_type='child').count()
    total_parents = User.objects.filter(user_type='parent').count()
    total_teachers = User.objects.filter(user_type='teacher').count()
    
    # Statistiques des exercices
    total_exercises = Exercise.objects.count()
    total_attempts = ExerciseAttempt.objects.filter(is_completed=True).count()
    
    # Statistiques par type de trouble
    dyslexia_exercises = Exercise.objects.filter(
        exercise_type__disorder_type__in=['dyslexia', 'both']
    ).count()
    
    dyscalculia_exercises = Exercise.objects.filter(
        exercise_type__disorder_type__in=['dyscalculia', 'both']
    ).count()
    
    # Utilisateurs récemment inscrits
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Tentatives récentes
    recent_attempts = ExerciseAttempt.objects.filter(
        is_completed=True
    ).order_by('-completed_at')[:10]
    
    context = {
        'total_users': total_users,
        'total_children': total_children,
        'total_parents': total_parents,
        'total_teachers': total_teachers,
        'total_exercises': total_exercises,
        'total_attempts': total_attempts,
        'dyslexia_exercises': dyslexia_exercises,
        'dyscalculia_exercises': dyscalculia_exercises,
        'recent_users': recent_users,
        'recent_attempts': recent_attempts
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)
