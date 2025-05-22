from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    ExerciseCategory, ExerciseType, Exercise, Question, Answer,
    ExerciseAttempt, QuestionResponse
)
from accounts.models import ChildProfile

User = get_user_model()

class ExerciseModelTest(TestCase):
    """
    Tests pour les modèles d'exercices
    """
    def setUp(self):
        # Créer une catégorie
        self.category = ExerciseCategory.objects.create(
            name='Lecture',
            description='Exercices de lecture',
            icon='fa-book-reader',
            color='#4E54C8'
        )
        
        # Créer un type d'exercice
        self.exercise_type = ExerciseType.objects.create(
            name='Reconnaissance de lettres',
            category=self.category,
            description='Exercices pour reconnaître les lettres',
            disorder_type='dyslexia',
            icon='fa-font'
        )
        
        # Créer un exercice
        self.exercise = Exercise.objects.create(
            title='Lettres similaires: b, d, p, q',
            exercise_type=self.exercise_type,
            instructions='Instructions pour l\'exercice',
            difficulty=1,
            estimated_time=10,
            points=50
        )
        
        # Créer une question
        self.question = Question.objects.create(
            exercise=self.exercise,
            question_text='Quelle est cette lettre? b',
            question_type='multiple_choice',
            order=1
        )
        
        # Créer des réponses
        self.answer_correct = Answer.objects.create(
            question=self.question,
            answer_text='b',
            is_correct=True,
            feedback='Bravo!',
            order=1
        )
        
        self.answer_incorrect = Answer.objects.create(
            question=self.question,
            answer_text='d',
            is_correct=False,
            feedback='Ce n\'est pas la bonne réponse.',
            order=2
        )
    
    def test_category_creation(self):
        """
        Teste la création d'une catégorie
        """
        self.assertEqual(self.category.name, 'Lecture')
        self.assertEqual(self.category.icon, 'fa-book-reader')
        self.assertEqual(self.category.color, '#4E54C8')
    
    def test_exercise_type_creation(self):
        """
        Teste la création d'un type d'exercice
        """
        self.assertEqual(self.exercise_type.name, 'Reconnaissance de lettres')
        self.assertEqual(self.exercise_type.category, self.category)
        self.assertEqual(self.exercise_type.disorder_type, 'dyslexia')
    
    def test_exercise_creation(self):
        """
        Teste la création d'un exercice
        """
        self.assertEqual(self.exercise.title, 'Lettres similaires: b, d, p, q')
        self.assertEqual(self.exercise.exercise_type, self.exercise_type)
        self.assertEqual(self.exercise.difficulty, 1)
        self.assertEqual(self.exercise.points, 50)
    
    def test_question_creation(self):
        """
        Teste la création d'une question
        """
        self.assertEqual(self.question.exercise, self.exercise)
        self.assertEqual(self.question.question_text, 'Quelle est cette lettre? b')
        self.assertEqual(self.question.question_type, 'multiple_choice')
        self.assertEqual(self.question.order, 1)
    
    def test_answer_creation(self):
        """
        Teste la création de réponses
        """
        self.assertEqual(self.answer_correct.question, self.question)
        self.assertEqual(self.answer_correct.answer_text, 'b')
        self.assertTrue(self.answer_correct.is_correct)
        
        self.assertEqual(self.answer_incorrect.question, self.question)
        self.assertEqual(self.answer_incorrect.answer_text, 'd')
        self.assertFalse(self.answer_incorrect.is_correct)


class ExerciseAttemptTest(TestCase):
    """
    Tests pour les tentatives d'exercices
    """
    def setUp(self):
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password123',
            user_type='child'
        )
        
        # Créer un profil enfant
        self.child_profile = ChildProfile.objects.create(
            user=self.user,
            school_level='ce2',
            has_dyslexia=True,
            dyslexia_level=2,
            has_dyscalculia=False
        )
        
        # Créer une catégorie
        self.category = ExerciseCategory.objects.create(
            name='Lecture',
            description='Exercices de lecture'
        )
        
        # Créer un type d'exercice
        self.exercise_type = ExerciseType.objects.create(
            name='Reconnaissance de lettres',
            category=self.category,
            disorder_type='dyslexia'
        )
        
        # Créer un exercice
        self.exercise = Exercise.objects.create(
            title='Test Exercise',
            exercise_type=self.exercise_type,
            instructions='Instructions',
            difficulty=1,
            points=50
        )
        
        # Créer une question
        self.question = Question.objects.create(
            exercise=self.exercise,
            question_text='Test Question',
            question_type='multiple_choice'
        )
        
        # Créer des réponses
        self.answer_correct = Answer.objects.create(
            question=self.question,
            answer_text='Correct',
            is_correct=True
        )
        
        self.answer_incorrect = Answer.objects.create(
            question=self.question,
            answer_text='Incorrect',
            is_correct=False
        )
        
        # Créer une tentative
        self.attempt = ExerciseAttempt.objects.create(
            user=self.user,
            exercise=self.exercise,
            started_at=timezone.now(),
            max_score=100
        )
    
    def test_attempt_creation(self):
        """
        Teste la création d'une tentative
        """
        self.assertEqual(self.attempt.user, self.user)
        self.assertEqual(self.attempt.exercise, self.exercise)
        self.assertEqual(self.attempt.score, 0)
        self.assertEqual(self.attempt.max_score, 100)
        self.assertFalse(self.attempt.is_completed)
    
    def test_question_response(self):
        """
        Teste la création d'une réponse à une question
        """
        # Créer une réponse correcte
        response_correct = QuestionResponse.objects.create(
            attempt=self.attempt,
            question=self.question,
            answer=self.answer_correct,
            is_correct=True,
            response_time=10
        )
        
        self.assertEqual(response_correct.attempt, self.attempt)
        self.assertEqual(response_correct.question, self.question)
        self.assertEqual(response_correct.answer, self.answer_correct)
        self.assertTrue(response_correct.is_correct)
        
        # Créer une réponse incorrecte
        response_incorrect = QuestionResponse.objects.create(
            attempt=self.attempt,
            question=self.question,
            answer=self.answer_incorrect,
            is_correct=False,
            response_time=15
        )
        
        self.assertEqual(response_incorrect.attempt, self.attempt)
        self.assertEqual(response_incorrect.question, self.question)
        self.assertEqual(response_incorrect.answer, self.answer_incorrect)
        self.assertFalse(response_incorrect.is_correct)


class ExerciseViewTest(TestCase):
    """
    Tests pour les vues d'exercices
    """
    def setUp(self):
        self.client = Client()
        
        # Créer un utilisateur
        self.user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password123',
            user_type='child'
        )
        
        # Créer un profil enfant
        self.child_profile = ChildProfile.objects.create(
            user=self.user,
            school_level='ce2',
            has_dyslexia=True,
            dyslexia_level=2,
            has_dyscalculia=False
        )
        
        # Créer une catégorie
        self.category = ExerciseCategory.objects.create(
            name='Lecture',
            description='Exercices de lecture'
        )
        
        # Créer un type d'exercice
        self.exercise_type = ExerciseType.objects.create(
            name='Reconnaissance de lettres',
            category=self.category,
            disorder_type='dyslexia'
        )
        
        # Créer un exercice
        self.exercise = Exercise.objects.create(
            title='Test Exercise',
            exercise_type=self.exercise_type,
            instructions='Instructions',
            difficulty=1,
            points=50
        )
    
    def test_exercise_list_requires_login(self):
        """
        Teste que la liste des exercices nécessite une connexion
        """
        response = self.client.get(reverse('exercises:exercise_list'))
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
    
    def test_exercise_list_logged_in(self):
        """
        Teste l'accès à la liste des exercices lorsque l'utilisateur est connecté
        """
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse('exercises:exercise_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercises/exercise_list.html')
        self.assertContains(response, 'Test Exercise')
    
    def test_exercise_detail_requires_login(self):
        """
        Teste que le détail d'un exercice nécessite une connexion
        """
        response = self.client.get(reverse('exercises:exercise_detail', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
    
    def test_exercise_detail_logged_in(self):
        """
        Teste l'accès au détail d'un exercice lorsque l'utilisateur est connecté
        """
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse('exercises:exercise_detail', args=[self.exercise.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'exercises/exercise_detail.html')
        self.assertContains(response, 'Test Exercise')
