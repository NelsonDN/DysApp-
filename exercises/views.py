from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, Count, Avg
import json

from .models import (
    ExerciseCategory, ExerciseType, Exercise, Question, Answer,
    ExerciseAttempt, QuestionResponse
)
from accounts.models import ChildProfile
from progress.models import ProgressRecord, Achievement, UserAchievement

from django.contrib.auth import get_user_model
User = get_user_model()

@login_required
def exercise_list(request):
    """
    Affiche la liste des exercices disponibles
    """
    # Récupérer les filtres
    category_id = request.GET.get('category')
    disorder = request.GET.get('disorder')
    difficulty = request.GET.get('difficulty')
    
    # Récupérer toutes les catégories pour le filtre
    categories = ExerciseCategory.objects.all()
    
    # Filtrer les exercices
    exercises = Exercise.objects.filter(is_active=True)
    
    if category_id:
        exercises = exercises.filter(exercise_type__category_id=category_id)
    
    if disorder:
        if disorder == 'dyslexia':
            exercises = exercises.filter(exercise_type__disorder_type__in=['dyslexia', 'both'])
        elif disorder == 'dyscalculia':
            exercises = exercises.filter(exercise_type__disorder_type__in=['dyscalculia', 'both'])
    
    if difficulty:
        exercises = exercises.filter(difficulty=difficulty)
    
    # Si l'utilisateur est un enfant, filtrer selon ses troubles
    if request.user.is_child:
        child_profile = request.user.child_profile
        
        if child_profile.has_dyslexia and child_profile.has_dyscalculia:
            # Les deux troubles, pas besoin de filtrer
            pass
        elif child_profile.has_dyslexia:
            # Seulement dyslexie
            exercises = exercises.filter(exercise_type__disorder_type__in=['dyslexia', 'both'])
        elif child_profile.has_dyscalculia:
            # Seulement dyscalculie
            exercises = exercises.filter(exercise_type__disorder_type__in=['dyscalculia', 'both'])
    
    # Récupérer les exercices complétés par l'utilisateur
    completed_exercises = ExerciseAttempt.objects.filter(
        user=request.user,
        is_completed=True
    ).values_list('exercise_id', flat=True)
    
    context = {
        'exercises': exercises,
        'categories': categories,
        'selected_category': category_id,
        'selected_disorder': disorder,
        'selected_difficulty': difficulty,
        'completed_exercises': completed_exercises
    }
    
    return render(request, 'exercises/exercise_list.html', context)

@login_required
def exercise_detail(request, exercise_id):
    """
    Affiche les détails d'un exercice et permet de le commencer
    """
    exercise = get_object_or_404(Exercise, id=exercise_id, is_active=True)
    
    # Vérifier si l'exercice est adapté au profil de l'enfant
    if request.user.is_child:
        child_profile = request.user.child_profile
        
        if (exercise.exercise_type.disorder_type == 'dyslexia' and not child_profile.has_dyslexia) or \
           (exercise.exercise_type.disorder_type == 'dyscalculia' and not child_profile.has_dyscalculia):
            messages.warning(request, _("Cet exercice n'est pas adapté à votre profil."))
    
    # Créer une nouvelle tentative si l'utilisateur clique sur "Commencer"
    if request.method == 'POST':
        attempt = ExerciseAttempt.objects.create(
            user=request.user,
            exercise=exercise,
            max_score=exercise.questions.count() * 10  # 10 points par question
        )
        
        # Rediriger vers la page de l'exercice
        if exercise.exercise_type.disorder_type == 'dyslexia':
            return redirect('exercises:dyslexia_exercise', attempt_id=attempt.id)
        else:
            return redirect('exercises:dyscalculia_exercise', attempt_id=attempt.id)
    
    # Récupérer les tentatives précédentes de l'utilisateur pour cet exercice
    previous_attempts = ExerciseAttempt.objects.filter(
        user=request.user,
        exercise=exercise,
        is_completed=True
    ).order_by('-completed_at')
    
    context = {
        'exercise': exercise,
        'previous_attempts': previous_attempts
    }
    
    return render(request, 'exercises/exercise_detail.html', context)

@login_required
def dyslexia_exercise(request, attempt_id):
    """
    Affiche et gère un exercice de dyslexie
    """
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    exercise = attempt.exercise
    
    # Vérifier si l'exercice est bien de type dyslexie
    if exercise.exercise_type.disorder_type not in ['dyslexia', 'both']:
        messages.error(request, _("Cet exercice n'est pas de type dyslexie."))
        return redirect('exercises:exercise_list')
    
    # Vérifier si l'exercice est déjà terminé
    if attempt.is_completed:
        return redirect('exercises:exercise_result', attempt_id=attempt.id)
    
    context = {
        'attempt': attempt,
        'exercise': exercise
    }
    
    return render(request, 'exercises/dyslexia_exercise.html', context)

@login_required
def dyscalculia_exercise(request, attempt_id):
    """
    Affiche et gère un exercice de dyscalculie
    """
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    exercise = attempt.exercise
    
    # Vérifier si l'exercice est bien de type dyscalculie
    if exercise.exercise_type.disorder_type not in ['dyscalculia', 'both']:
        messages.error(request, _("Cet exercice n'est pas de type dyscalculie."))
        return redirect('exercises:exercise_list')
    
    # Vérifier si l'exercice est déjà terminé
    if attempt.is_completed:
        return redirect('exercises:exercise_result', attempt_id=attempt.id)
    
    context = {
        'attempt': attempt,
        'exercise': exercise
    }
    
    return render(request, 'exercises/dyscalculia_exercise.html', context)

@login_required
def get_question(request, attempt_id, question_index):
    """
    API pour récupérer une question spécifique d'un exercice
    """
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    exercise = attempt.exercise
    
    # Récupérer toutes les questions de l'exercice
    questions = list(exercise.questions.all().order_by('order'))
    
    # Vérifier si l'index de la question est valide
    if question_index < 0 or question_index >= len(questions):
        return JsonResponse({
            'type': 'error',
            'message': _("Question non trouvée.")
        })
    
    # Récupérer la question
    question = questions[question_index]
    
    # Vérifier si la question a déjà été répondue
    previous_response = QuestionResponse.objects.filter(
        attempt=attempt,
        question=question
    ).first()
    
    # Préparer les données de la question
    question_data = {
        'id': question.id,
        'text': question.question_text,
        'question_type': question.question_type,
        'current_index': question_index,
        'total_questions': len(questions),
        'already_answered': previous_response is not None,
        'was_correct': previous_response.is_correct if previous_response else None,
        'previous_answer': previous_response.answer_id if previous_response and previous_response.answer else None
    }
    
    # Ajouter l'image si elle existe
    if question.image:
        question_data['image'] = question.image.url
    
    # Ajouter l'audio si il existe
    if question.audio:
        question_data['audio'] = question.audio.url
    
    # Ajouter les réponses possibles
    if question.question_type in ['multiple_choice', 'matching', 'drag_drop']:
        answers = []
        for answer in question.answers.all().order_by('order'):
            answer_data = {
                'id': answer.id,
                'text': answer.answer_text
            }
            
            if answer.image:
                answer_data['image'] = answer.image.url
            
            answers.append(answer_data)
        
        question_data['answers'] = answers
    
    return JsonResponse(question_data)


# Dans views.py, remplacez la fonction submit_answer par cette version corrigée :

@login_required
def submit_answer(request, attempt_id):
    """
    Gère la soumission des réponses aux questions d'exercice
    """
    if request.method != 'POST':
        return JsonResponse({
            'type': 'error',
            'message': _("Méthode non autorisée.")
        })
    
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    
    # Vérifier si l'exercice est déjà terminé
    if attempt.is_completed:
        return JsonResponse({
            'type': 'error',
            'message': _("Cet exercice est déjà terminé.")
        })
    
    # Récupérer les données de la requête
    try:
        data = json.loads(request.body)
        print("Données reçues:", data)  # Debug
    except json.JSONDecodeError:
        return JsonResponse({
            'type': 'error',
            'message': _("Données invalides.")
        })
    
    # Vérifier si c'est une demande de complétion d'exercice
    if data.get('type') == 'complete_exercise':
        return complete_exercise(request, attempt)
    
    # Récupérer les données de la réponse
    question_id = data.get('question_id')
    answer_id = data.get('answer_id')
    text_response = data.get('text_response', "")  # Valeur par défaut
    
    print(f"Question ID: {question_id}, Answer ID: {answer_id}, Text: '{text_response}'")  # Debug
    
    # Vérifier si la question existe
    try:
        question = get_object_or_404(Question, id=question_id, exercise=attempt.exercise)
        print(f"Question trouvée: {question.question_text}")  # Debug
    except:
        return JsonResponse({
            'type': 'error',
            'message': _("Question non trouvée.")
        })
    
    # Vérifier si la question a déjà été répondue
    existing_response = QuestionResponse.objects.filter(
        attempt=attempt,
        question=question
    ).first()
    
    if existing_response:
        return JsonResponse({
            'type': 'error',
            'message': _("Vous avez déjà répondu à cette question.")
        })
    
    # Traiter la réponse en fonction du type de question
    is_correct = False
    answer = None
    feedback_message = ""
    
    print(f"Type de question: {question.question_type}")  # Debug
    
    if question.question_type in ['multiple_choice', 'true_false']:
        if answer_id:
            try:
                answer = get_object_or_404(Answer, id=answer_id, question=question)
                is_correct = answer.is_correct
                feedback_message = answer.feedback if answer.feedback else (
                    "Bonne réponse !" if is_correct else "Réponse incorrecte."
                )
                print(f"Réponse trouvée: {answer.answer_text}, Correcte: {is_correct}")  # Debug
            except:
                return JsonResponse({
                    'type': 'error',
                    'message': _("Réponse non trouvée.")
                })
        else:
            return JsonResponse({
                'type': 'error',
                'message': _("Veuillez sélectionner une réponse.")
            })
    
    elif question.question_type == 'fill_blank':
        if text_response and text_response.strip():
            # Vérifier si la réponse textuelle est correcte
            correct_answers = question.answers.filter(is_correct=True).values_list('answer_text', flat=True)
            user_answer = text_response.strip()
            
            # Vérification flexible (nombre ou texte)
            is_correct = False
            for correct_answer in correct_answers:
                if user_answer.lower() == correct_answer.lower():
                    is_correct = True
                    break
                # Pour les réponses numériques
                try:
                    if float(user_answer) == float(correct_answer):
                        is_correct = True
                        break
                except (ValueError, TypeError):
                    pass
            
            # Message de feedback personnalisé pour les math
            if is_correct:
                feedback_message = "Excellent ! C'est la bonne réponse."
            else:
                correct_answer = correct_answers[0] if correct_answers else "?"
                feedback_message = f"Pas tout à fait. La bonne réponse était : {correct_answer}"
                
            print(f"Réponse textuelle: '{user_answer}', Correcte: {is_correct}")  # Debug
        else:
            return JsonResponse({
                'type': 'error',
                'message': _("Veuillez saisir une réponse.")
            })
    
    # Créer la réponse
    try:
        response = QuestionResponse.objects.create(
            attempt=attempt,
            question=question,
            answer=answer,
            text_response=text_response if text_response else "",
            is_correct=is_correct,
            response_time=30
        )
        print(f"Réponse créée avec succès: ID {response.id}")  # Debug
    except Exception as e:
        print(f"Erreur lors de la création de la réponse: {str(e)}")  # Debug
        return JsonResponse({
            'type': 'error',
            'message': f"Erreur lors de la sauvegarde: {str(e)}"
        })
    
    # Mettre à jour le score de la tentative
    if is_correct:
        attempt.score += 10
        attempt.save()
        print(f"Score mis à jour: {attempt.score}")  # Debug
    
    # Vérifier si toutes les questions ont été répondues
    total_questions = attempt.exercise.questions.count()
    answered_questions = attempt.responses.count()
    
    print(f"Questions répondues: {answered_questions}/{total_questions}")  # Debug
    
    # Préparer la réponse
    response_data = {
        'is_correct': is_correct,
        'score': attempt.score,
        'feedback': feedback_message,
        'completed': answered_questions >= total_questions
    }
    
    print(f"Réponse envoyée: {response_data}")  # Debug
    return JsonResponse(response_data)


# @login_required
# def submit_answer(request, attempt_id):
#     """
#     Gère la soumission des réponses aux questions d'exercice
#     """
#     if request.method != 'POST':
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Méthode non autorisée.")
#         })
    
#     attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    
#     # Vérifier si l'exercice est déjà terminé
#     if attempt.is_completed:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Cet exercice est déjà terminé.")
#         })
    
#     # Récupérer les données de la requête
#     try:
#         data = json.loads(request.body)
#         print("Données reçues:", data)  # Debug
#     except json.JSONDecodeError:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Données invalides.")
#         })
    
#     # Vérifier si c'est une demande de complétion d'exercice
#     if data.get('type') == 'complete_exercise':
#         return complete_exercise(request, attempt)
    
#     # Récupérer les données de la réponse
#     question_id = data.get('question_id')
#     answer_id = data.get('answer_id')
#     text_response = data.get('text_response')
    
#     # CORRECTION : Gérer text_response None
#     if text_response is None:
#         text_response = ""
    
#     print(f"Question ID: {question_id}, Answer ID: {answer_id}, Text: '{text_response}'")  # Debug
    
#     # Vérifier si la question existe
#     try:
#         question = get_object_or_404(Question, id=question_id, exercise=attempt.exercise)
#         print(f"Question trouvée: {question.question_text}")  # Debug
#     except:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Question non trouvée.")
#         })
    
#     # Vérifier si la question a déjà été répondue
#     existing_response = QuestionResponse.objects.filter(
#         attempt=attempt,
#         question=question
#     ).first()
    
#     if existing_response:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Vous avez déjà répondu à cette question.")
#         })
    
#     # Traiter la réponse en fonction du type de question
#     is_correct = False
#     answer = None
    
#     print(f"Type de question: {question.question_type}")  # Debug
    
#     if question.question_type in ['multiple_choice', 'true_false']:
#         if answer_id:
#             try:
#                 answer = get_object_or_404(Answer, id=answer_id, question=question)
#                 is_correct = answer.is_correct
#                 print(f"Réponse trouvée: {answer.answer_text}, Correcte: {is_correct}")  # Debug
#             except:
#                 return JsonResponse({
#                     'type': 'error',
#                     'message': _("Réponse non trouvée.")
#                 })
#         else:
#             return JsonResponse({
#                 'type': 'error',
#                 'message': _("Veuillez sélectionner une réponse.")
#             })
    
#     elif question.question_type == 'fill_blank':
#         if text_response and text_response.strip():
#             # Vérifier si la réponse textuelle est correcte
#             correct_answers = question.answers.filter(is_correct=True).values_list('answer_text', flat=True)
#             is_correct = text_response.strip().lower() in [ans.lower() for ans in correct_answers]
#         else:
#             return JsonResponse({
#                 'type': 'error',
#                 'message': _("Veuillez saisir une réponse.")
#             })
    
#     # Créer la réponse
#     try:
#         response = QuestionResponse.objects.create(
#             attempt=attempt,
#             question=question,
#             answer=answer,
#             text_response=text_response,
#             is_correct=is_correct,
#             response_time=30
#         )
#         print(f"Réponse créée avec succès: ID {response.id}")  # Debug
#     except Exception as e:
#         print(f"Erreur lors de la création de la réponse: {str(e)}")  # Debug
#         return JsonResponse({
#             'type': 'error',
#             'message': f"Erreur lors de la sauvegarde: {str(e)}"
#         })
    
#     # Mettre à jour le score de la tentative
#     if is_correct:
#         attempt.score += 10
#         attempt.save()
#         print(f"Score mis à jour: {attempt.score}")  # Debug
    
#     # Vérifier si toutes les questions ont été répondues
#     total_questions = attempt.exercise.questions.count()
#     answered_questions = attempt.responses.count()
    
#     print(f"Questions répondues: {answered_questions}/{total_questions}")  # Debug
    
#     # Préparer la réponse
#     response_data = {
#         'is_correct': is_correct,
#         'score': attempt.score,
#         'feedback': answer.feedback if answer else None,
#         'completed': answered_questions >= total_questions
#     }
    
#     print(f"Réponse envoyée: {response_data}")  # Debug
#     return JsonResponse(response_data)

# @login_required
# def submit_answer(request, attempt_id):
#     """
#     Gère la soumission des réponses aux questions d'exercice
#     """
#     # Débogage
#     print("Données reçues:", request.body.decode('utf-8'))
#     """
#     API pour soumettre une réponse à une question
#     """
#     if request.method != 'POST':
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Méthode non autorisée.")
#         })
#     print("Méthode POST")
    
#     attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
#     print("EXERCISE RECUPERER")
    
#     # Vérifier si l'exercice est déjà terminé
#     if attempt.is_completed:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Cet exercice est déjà terminé.")
#         })
#     print("Vérifier si l'exercice est déjà terminé")
    
#     # Récupérer les données de la requête
#     try:
#         data = json.loads(request.body)
#         print("BONNNNNNNNNNNNNNNNN")
#         print(data)
#         print("OKAYYYYY")
#     except json.JSONDecodeError:
#         print("ERREURRRRR de décodage JSON")
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Données invalides.")
#         })
    
#     # Vérifier si c'est une demande de complétion d'exercice
#     if data.get('type') == 'complete_exercise':
#         return complete_exercise(request, attempt)
    
#     # Récupérer les données de la réponse
#     question_id = data.get('question_id')
#     answer_id = data.get('answer_id')
#     text_response = data.get('text_response')
#     print("ON A RECUPERER LES DONNEES DE LA REPONSE")
#     print(question_id, answer_id, text_response)
    
#     # Vérifier si la question existe
#     question = get_object_or_404(Question, id=question_id, exercise=attempt.exercise)
#     print("ON A RECUPERER LA QUESTION")
    
#     # Vérifier si la question a déjà été répondue
#     existing_response = QuestionResponse.objects.filter(
#         attempt=attempt,
#         question=question
#     ).first()
#     print("ON A VERIFIER SI LA QUESTION A DEJA UNE REPONSE")
    
#     if existing_response:
#         return JsonResponse({
#             'type': 'error',
#             'message': _("Vous avez déjà répondu à cette question.")
#         })
#     print("ON A VERIFIER SI LA QUESTION A DEJA ETE REPONDU")
    
#     # Traiter la réponse en fonction du type de question
#     is_correct = False
#     answer = None
#     print(1111111111111111111)
    
#     if question.question_type in ['multiple_choice', 'true_false']:
#         # Vérifier si la réponse existe
#         answer = get_object_or_404(Answer, id=answer_id, question=question)
#         is_correct = answer.is_correct
#         print(2222222222222222222)
    
#     elif question.question_type == 'fill_blank':
#         # Vérifier si la réponse textuelle est correcte
#         correct_answers = question.answers.filter(is_correct=True).values_list('answer_text', flat=True)
#         is_correct = text_response in correct_answers
#         print(3333333333333333333333333)
    
#     # Créer la réponse
#     response = QuestionResponse.objects.create(
#         attempt=attempt,
#         question=question,
#         answer=answer,
#         text_response=text_response,
#         is_correct=is_correct,
#         response_time=30  # Valeur par défaut, à améliorer
#     )
#     print(44444444444444444444444444444444444)
    
#     # Mettre à jour le score de la tentative
#     if is_correct:
#         attempt.score += 10  # 10 points par question correcte
#         attempt.save()
#     print(5555555555555555555555555555555)
    
#     # Vérifier si toutes les questions ont été répondues
#     total_questions = attempt.exercise.questions.count()
#     answered_questions = attempt.responses.count()
#     print(6666666666666666666666666666)
    
#     # Préparer la réponse
#     response_data = {
#         'is_correct': is_correct,
#         'score': attempt.score,
#         'feedback': answer.feedback if answer else None,
#         'completed': answered_questions >= total_questions
#     }
#     print(7777777777777777777777777777)
    
#     return JsonResponse(response_data)

def complete_exercise(request, attempt):
    """
    Termine un exercice et met à jour les données associées
    """
    # Calculer le temps passé
    time_spent = (timezone.now() - attempt.started_at).total_seconds()
    
    # Mettre à jour la tentative
    attempt.is_completed = True
    attempt.completed_at = timezone.now()
    attempt.time_spent = time_spent
    attempt.save()
    
    # Mettre à jour le profil de l'enfant
    if request.user.is_child:
        child_profile = request.user.child_profile
        child_profile.points += attempt.score
        child_profile.update_level()
    
    # Mettre à jour les enregistrements de progression
    progress_record, created = ProgressRecord.objects.get_or_create(
        user=request.user,
        exercise_type=attempt.exercise.exercise_type,
        defaults={
            'skill_level': 1,
            'exercises_completed': 0
        }
    )
    
    progress_record.exercises_completed += 1
    
    # Calculer le niveau de compétence basé sur les tentatives récentes
    recent_attempts = ExerciseAttempt.objects.filter(
        user=request.user,
        exercise__exercise_type=attempt.exercise.exercise_type,
        is_completed=True
    ).order_by('-completed_at')[:5]
    
    if recent_attempts:
        avg_score = sum([a.score_percentage for a in recent_attempts]) / len(recent_attempts)
        progress_record.skill_level = min(10, max(1, int(avg_score / 10)))
    
    progress_record.save()
    
    # Vérifier les récompenses
    check_achievements(request.user, attempt)
    
    return JsonResponse({
        'status': 'success',
        'message': _("Exercice terminé avec succès."),
        'redirect_url': f"/exercises/result/{attempt.id}/"
    })

def check_achievements(user, attempt):
    """
    Vérifie si l'utilisateur a gagné des récompenses
    """
    # Vérifier si c'est la première tentative complétée
    if ExerciseAttempt.objects.filter(user=user, is_completed=True).count() == 1:
        # Premier pas
        achievement = Achievement.objects.get(name="Premier pas")
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # Vérifier si l'utilisateur a obtenu un score parfait
    if attempt.score == attempt.max_score:
        # Score parfait
        achievement = Achievement.objects.get(name="Score parfait")
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # Vérifier le nombre d'exercices de lecture complétés
    reading_attempts = ExerciseAttempt.objects.filter(
        user=user,
        exercise__exercise_type__category__name='Lecture',
        is_completed=True
    ).count()
    
    if reading_attempts >= 5:
        # Apprenti lecteur
        achievement = Achievement.objects.get(name="Apprenti lecteur")
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)
    
    # Vérifier le nombre d'exercices de mathématiques complétés
    math_attempts = ExerciseAttempt.objects.filter(
        user=user,
        exercise__exercise_type__category__name__in=['Nombres', 'Calcul', 'Problèmes'],
        is_completed=True
    ).count()
    
    if math_attempts >= 5:
        # Maître des nombres
        achievement = Achievement.objects.get(name="Maître des nombres")
        UserAchievement.objects.get_or_create(user=user, achievement=achievement)

@login_required
def exercise_result(request, attempt_id):
    """
    Affiche les résultats d'un exercice terminé
    """
    attempt = get_object_or_404(ExerciseAttempt, id=attempt_id, user=request.user)
    
    # Vérifier si l'exercice est terminé
    if not attempt.is_completed:
        messages.error(request, _("Cet exercice n'est pas encore terminé."))
        return redirect('exercises:exercise_detail', exercise_id=attempt.exercise.id)
    
    # Calculer les statistiques
    total_questions = attempt.exercise.questions.count()
    correct_answers = attempt.responses.filter(is_correct=True).count()
    score_percentage = (attempt.score / attempt.max_score) * 100 if attempt.max_score > 0 else 0
    
    # Récupérer les récompenses gagnées
    achievements = UserAchievement.objects.filter(
        user=request.user,
        date_earned__gte=attempt.started_at,
        date_earned__lte=attempt.completed_at + timezone.timedelta(minutes=5)
    )
    
    # Recommander d'autres exercices
    recommended_exercises = Exercise.objects.filter(
        exercise_type__disorder_type=attempt.exercise.exercise_type.disorder_type,
        is_active=True
    ).exclude(id=attempt.exercise.id).order_by('?')[:3]
    
    context = {
        'attempt': attempt,
        'total_questions': total_questions,
        'correct_answers': correct_answers,
        'score_percentage': score_percentage,
        'achievements': achievements,
        'recommended_exercises': recommended_exercises
    }
    
    return render(request, 'exercises/exercise_result.html', context)
