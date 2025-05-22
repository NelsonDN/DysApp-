from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Avg, Sum, Q
from datetime import timedelta

from .models import (
    ProgressRecord, ProgressReport, Achievement, UserAchievement,
    RewardItem, UserReward
)
from accounts.models import ChildProfile
from exercises.models import ExerciseAttempt, Exercise, ExerciseType

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def progress_report(request):
    """
    Affiche le rapport de progression de l'utilisateur
    """
    user = request.user
    
    # Si l'utilisateur est un parent ou un enseignant, rediriger vers la liste des enfants/élèves
    if user.is_parent:
        return redirect('progress:children_progress')
    elif user.is_teacher:
        return redirect('progress:students_progress')
    
    # Récupérer les enregistrements de progression
    progress_records = ProgressRecord.objects.filter(user=user).order_by('exercise_type__category', 'exercise_type__name')
    
    # Récupérer les tentatives d'exercices
    attempts = ExerciseAttempt.objects.filter(user=user, is_completed=True).order_by('-completed_at')
    
    # Calculer les statistiques
    total_attempts = attempts.count()
    avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
    total_time = attempts.aggregate(sum=Sum('time_spent'))['sum'] or 0
    
    # Calculer les statistiques par catégorie
    categories = {}
    
    for record in progress_records:
        category = record.exercise_type.category
        
        if category.id not in categories:
            categories[category.id] = {
                'category': category,
                'records': [],
                'avg_skill_level': 0,
                'total_exercises': 0
            }
        
        categories[category.id]['records'].append(record)
        categories[category.id]['total_exercises'] += record.exercises_completed
    
    # Calculer le niveau de compétence moyen par catégorie
    for category_id, data in categories.items():
        if data['records']:
            data['avg_skill_level'] = sum([r.skill_level for r in data['records']]) / len(data['records'])
    
    # Récupérer les récompenses
    achievements = UserAchievement.objects.filter(user=user).order_by('-date_earned')
    
    # Récupérer le profil enfant
    child_profile = getattr(user, 'child_profile', None)

    # Calculer les statistiques manquantes
    total_exercises_completed = sum([record.exercises_completed for record in progress_records])
    total_achievements = achievements.count()

    # Calculer la répartition par type d'exercice (vous devrez adapter selon votre modèle ExerciseType)
    dyslexia_exercises = attempts.filter(exercise__exercise_type__category__name__icontains='dyslexie')
    dyscalculia_exercises = attempts.filter(exercise__exercise_type__category__name__icontains='dyscalculie')
    mixed_exercises = attempts.exclude(
        Q(exercise__exercise_type__category__name__icontains='dyslexie') |
        Q(exercise__exercise_type__category__name__icontains='dyscalculie')
    )

    dyslexia_exercises_count = dyslexia_exercises.count()
    dyscalculia_exercises_count = dyscalculia_exercises.count()
    mixed_exercises_count = mixed_exercises.count()

    # Calculer les pourcentages
    total_for_percentage = max(total_attempts, 1)  # Éviter division par zéro
    dyslexia_percentage = round((dyslexia_exercises_count / total_for_percentage) * 100, 1)
    dyscalculia_percentage = round((dyscalculia_exercises_count / total_for_percentage) * 100, 1)
    mixed_percentage = round((mixed_exercises_count / total_for_percentage) * 100, 1)

    # Récupérer les tentatives récentes et les récompenses récentes
    recent_attempts = attempts[:5]  # 5 dernières tentatives
    recent_achievements = achievements[:5]  # 5 dernières récompenses

    context = {
        'user_profile': child_profile,
        'progress_records': progress_records,
        'attempts': attempts,
        'recent_attempts': recent_attempts,
        'recent_achievements': recent_achievements,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'total_time': total_time,
        'total_exercises_completed': total_exercises_completed,
        'total_achievements': total_achievements,
        'categories': categories.values(),
        'achievements': achievements,
        'dyslexia_exercises_count': dyslexia_exercises_count,
        'dyscalculia_exercises_count': dyscalculia_exercises_count,
        'mixed_exercises_count': mixed_exercises_count,
        'dyslexia_percentage': dyslexia_percentage,
        'dyscalculia_percentage': dyscalculia_percentage,
        'mixed_percentage': mixed_percentage,
    }
    
    return render(request, 'progress/progress_report.html', context)

@login_required
def children_progress(request):
    """
    Affiche la progression des enfants d'un parent
    """
    if not request.user.is_parent:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    parent_profile = request.user.parent_profile
    children = parent_profile.children.all()
    
    # Récupérer les statistiques pour chaque enfant
    children_stats = []
    
    for child in children:
        child_profile = getattr(child, 'child_profile', None)

        
        if child_profile:
            # Récupérer les enregistrements de progression
            progress_records = ProgressRecord.objects.filter(user=child).order_by('exercise_type__category', 'exercise_type__name')
            
            # Récupérer les tentatives d'exercices
            attempts = ExerciseAttempt.objects.filter(user=child, is_completed=True).order_by('-completed_at')
            
            # Calculer les statistiques
            total_attempts = attempts.count()
            avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
            total_time = attempts.aggregate(sum=Sum('time_spent'))['sum'] or 0
            
            # Dans la boucle, après avoir calculé les statistiques de base, ajoutez :
            last_activity = attempts.first().completed_at if attempts.exists() else None

            # Calculer un pourcentage de progression (basé sur le niveau de compétence moyen)
            avg_skill_level = progress_records.aggregate(avg=Avg('skill_level'))['avg'] or 0
            progress_percentage = (avg_skill_level / 10) * 100  # Assuming max skill level is 10
                
            # Ajouter les statistiques
            children_stats.append({
                'child': child,
                'profile': child_profile,
                'progress_records': progress_records,
                'attempts': attempts[:5],  # Limiter à 5 tentatives
                'total_attempts': total_attempts,
                'avg_score': avg_score,
                'total_time': total_time,
                'last_activity': last_activity,
                'progress_percentage': progress_percentage, 
            })

    # Calculer les statistiques globales
    total_children = children.count()
    active_students = 0  # Enfants ayant fait des exercices dans les 30 derniers jours
    total_exercises = 0
    all_scores = []

    for stats in children_stats:
        total_exercises += stats['total_attempts']
        if stats['avg_score'] > 0:
            all_scores.append(stats['avg_score'])
        
        # Vérifier si l'enfant est actif (activité dans les 30 derniers jours)
        recent_activity = ExerciseAttempt.objects.filter(
            user=stats['child'], 
            completed_at__gte=timezone.now() - timedelta(days=30)
        ).exists()
        if recent_activity:
            active_students += 1

    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    context = {
        'children_stats': children_stats,
        'children': children,  # Ajouter cette ligne
        'total_children': total_children,
        'total_exercises': total_exercises,
        'avg_score': avg_score,
    }
    return render(request, 'progress/children_progress.html', context)

@login_required
def students_progress(request):
    """
    Affiche la progression des élèves d'un enseignant
    """
    if not request.user.is_teacher:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    teacher_profile = request.user.teacher_profile
    students = teacher_profile.students.all()
    
    # Récupérer les statistiques pour chaque élève
    students_stats = []
    
    for student in students:
        student_profile = getattr(student, 'child_profile', None)
        
        if student_profile:
            # Récupérer les enregistrements de progression
            progress_records = ProgressRecord.objects.filter(user=student).order_by('exercise_type__category', 'exercise_type__name')
            
            # Récupérer les tentatives d'exercices
            attempts = ExerciseAttempt.objects.filter(user=student, is_completed=True).order_by('-completed_at')
            
            # Calculer les statistiques
            total_attempts = attempts.count()
            avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
            total_time = attempts.aggregate(sum=Sum('time_spent'))['sum'] or 0

            # Dans la boucle, après avoir calculé les statistiques de base, ajoutez :
            last_activity = attempts.first().completed_at if attempts.exists() else None

            # Calculer un pourcentage de progression (basé sur le niveau de compétence moyen)
            avg_skill_level = progress_records.aggregate(avg=Avg('skill_level'))['avg'] or 0
            progress_percentage = (avg_skill_level / 10) * 100  # Assuming max skill level is 10

            
            # Ajouter les statistiques
            students_stats.append({
                'student': student,
                'profile': student_profile,
                'progress_records': progress_records,
                'attempts': attempts[:5],  # Limiter à 5 tentatives
                'total_attempts': total_attempts,
                'avg_score': avg_score,
                'total_time': total_time,
                'last_activity': last_activity,
                'progress_percentage': progress_percentage,
            })

    # Calculer les statistiques globales
    total_students = students.count()
    active_students = 0  # Élèves ayant fait des exercices dans les 30 derniers jours
    total_exercises = 0
    all_scores = []

    for stats in students_stats:
        total_exercises += stats['total_attempts']
        if stats['avg_score'] > 0:
            all_scores.append(stats['avg_score'])
        
        # Vérifier si l'élève est actif (activité dans les 30 derniers jours)
        recent_activity = ExerciseAttempt.objects.filter(
            user=stats['student'], 
            completed_at__gte=timezone.now() - timedelta(days=30)
        ).exists()
        if recent_activity:
            active_students += 1

    avg_score = sum(all_scores) / len(all_scores) if all_scores else 0

    context = {
        'students_stats': students_stats,
        'students': students,  # Ajouter cette ligne
        'total_students': total_students,
        'active_students': active_students,
        'total_exercises': total_exercises,
        'avg_score': avg_score,
    }
    
    return render(request, 'progress/students_progress.html', context)

@login_required
def child_progress(request, child_id):
    """
    Affiche la progression détaillée d'un enfant
    """
    # Vérifier si l'utilisateur est un parent ou un enseignant
    if not (request.user.is_parent or request.user.is_teacher):
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    # Vérifier si l'enfant est associé au parent ou à l'enseignant
    child = None
    
    if request.user.is_parent:
        parent_profile = request.user.parent_profile
        child = get_object_or_404(parent_profile.children, id=child_id)
    elif request.user.is_teacher:
        teacher_profile = request.user.teacher_profile
        child = get_object_or_404(teacher_profile.students, id=child_id)
    
    child_profile = getattr(child, 'child_profile', None)
    
    if not child_profile:
        messages.error(request, _("Profil enfant non trouvé."))
        return redirect('dashboard:dashboard')
    
    # Récupérer les enregistrements de progression
    progress_records = ProgressRecord.objects.filter(user=child).order_by('exercise_type__category', 'exercise_type__name')
    
    # Récupérer les tentatives d'exercices
    attempts = ExerciseAttempt.objects.filter(user=child, is_completed=True).order_by('-completed_at')
    
    # Calculer les statistiques
    total_attempts = attempts.count()
    avg_score = attempts.aggregate(avg=Avg('score'))['avg'] or 0
    total_time = attempts.aggregate(sum=Sum('time_spent'))['sum'] or 0
    
    # Calculer les statistiques par catégorie
    categories = {}
    
    for record in progress_records:
        category = record.exercise_type.category
        
        if category.id not in categories:
            categories[category.id] = {
                'category': category,
                'records': [],
                'avg_skill_level': 0,
                'total_exercises': 0
            }
        
        categories[category.id]['records'].append(record)
        categories[category.id]['total_exercises'] += record.exercises_completed
    
    # Calculer le niveau de compétence moyen par catégorie
    for category_id, data in categories.items():
        if data['records']:
            data['avg_skill_level'] = sum([r.skill_level for r in data['records']]) / len(data['records'])
    
    # Récupérer les récompenses
    achievements = UserAchievement.objects.filter(user=child).order_by('-date_earned')
    
    context = {
        'child': child,
        'child_profile': child_profile,
        'progress_records': progress_records,
        'attempts': attempts,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
        'total_time': total_time,
        'categories': categories.values(),
        'achievements': achievements
    }
    
    return render(request, 'progress/child_progress.html', context)

@login_required
def achievements(request):
    """
    Affiche les récompenses de l'utilisateur
    """
    user = request.user
    
    # Récupérer toutes les récompenses
    all_achievements = Achievement.objects.all().order_by('name')
    
    # Récupérer les récompenses de l'utilisateur
    user_achievements = UserAchievement.objects.filter(user=user).values_list('achievement_id', flat=True)
    
    # Préparer les données
    achievements_data = []
    
    for achievement in all_achievements:
        user_achievement = None
        
        if achievement.id in user_achievements:
            user_achievement = UserAchievement.objects.get(user=user, achievement=achievement)
        
        achievements_data.append({
            'achievement': achievement,
            'user_achievement': user_achievement,
            'is_earned': achievement.id in user_achievements
        })
    
    context = {
        'achievements_data': achievements_data
    }
    
    return render(request, 'progress/achievements.html', context)

@login_required
def rewards_shop(request):
    """
    Affiche la boutique de récompenses
    """
    user = request.user
    
    # Vérifier si l'utilisateur est un enfant
    if not user.is_child:
        messages.error(request, _("Seuls les enfants peuvent accéder à la boutique de récompenses."))
        return redirect('dashboard:dashboard')
    
    child_profile = user.child_profile
    
    # Récupérer les objets de récompense disponibles
    reward_items = RewardItem.objects.filter(is_active=True).order_by('points_cost')
    
    # Récupérer les récompenses de l'utilisateur
    user_rewards = UserReward.objects.filter(user=user).values_list('reward_id', flat=True)
    
    # Préparer les données
    rewards_data = []
    
    for item in reward_items:
        rewards_data.append({
            'item': item,
            'is_purchased': item.id in user_rewards,
            'can_afford': child_profile.points >= item.points_cost
        })
    
    context = {
        'child_profile': child_profile,
        'rewards_data': rewards_data
    }
    
    return render(request, 'progress/rewards_shop.html', context)

@login_required
def purchase_reward(request, reward_id):
    """
    Permet à un enfant d'acheter une récompense
    """
    user = request.user
    
    # Vérifier si l'utilisateur est un enfant
    if not user.is_child:
        messages.error(request, _("Seuls les enfants peuvent acheter des récompenses."))
        return redirect('dashboard:dashboard')
    
    child_profile = user.child_profile
    
    # Récupérer l'objet de récompense
    reward_item = get_object_or_404(RewardItem, id=reward_id, is_active=True)
    
    # Vérifier si l'utilisateur a déjà acheté cette récompense
    if UserReward.objects.filter(user=user, reward=reward_item).exists():
        messages.warning(request, _("Vous avez déjà acheté cette récompense."))
        return redirect('progress:rewards_shop')
    
    # Vérifier si l'utilisateur a assez de points
    if child_profile.points < reward_item.points_cost:
        messages.error(request, _("Vous n'avez pas assez de points pour acheter cette récompense."))
        return redirect('progress:rewards_shop')
    
    # Acheter la récompense
    UserReward.objects.create(user=user, reward=reward_item)
    
    # Déduire les points
    child_profile.points -= reward_item.points_cost
    child_profile.save()
    
    messages.success(request, _("Vous avez acheté la récompense avec succès !"))
    return redirect('progress:rewards_shop')
