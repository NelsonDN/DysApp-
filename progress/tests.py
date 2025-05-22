from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import (
    Achievement, UserAchievement, ProgressRecord, ProgressReport,
    RewardItem, UserReward
)
from accounts.models import ChildProfile
from exercises.models import (
    ExerciseCategory, ExerciseType, Exercise, ExerciseAttempt
)

User = get_user_model()

class AchievementModelTest(TestCase):
    """
    Tests pour les modèles de récompenses
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
        
        # Créer une récompense
        self.achievement = Achievement.objects.create(
            name='Test Achievement',
            description='Description de la récompense',
            icon='fa-trophy',
            points=10
        )
        
        # Attribuer la récompense à l'utilisateur
        self.user_achievement = UserAchievement.objects.create(
            user=self.user,
            achievement=self.achievement
        )
    
    def test_achievement_creation(self):
        """
        Teste la création d'une récompense
        """
        self.assertEqual(self.achievement.name, 'Test Achievement')
        self.assertEqual(self.achievement.icon, 'fa-trophy')
        self.assertEqual(self.achievement.points, 10)
    
    def test_user_achievement_creation(self):
        """
        Teste l'attribution d'une récompense à un utilisateur
        """
        self.assertEqual(self.user_achievement.user, self.user)
        self.assertEqual(self.user_achievement.achievement, self.achievement)


class ProgressRecordTest(TestCase):
    """
    Tests pour les enregistrements de progression
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
        
        # Créer un enregistrement de progression
        self.progress_record = ProgressRecord.objects.create(
            user=self.user,
            exercise_type=self.exercise_type,
            skill_level=3,
            exercises_completed=5
        )
    
    def test_progress_record_creation(self):
        """
        Teste la création d'un enregistrement de progression
        """
        self.assertEqual(self.progress_record.user, self.user)
        self.assertEqual(self.progress_record.exercise_type, self.exercise_type)
        self.assertEqual(self.progress_record.skill_level, 3)
        self.assertEqual(self.progress_record.exercises_completed, 5)


class RewardItemTest(TestCase):
    """
    Tests pour les objets de récompense
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
            has_dyscalculia=False,
            points=100
        )
        
        # Créer un objet de récompense
        self.reward_item = RewardItem.objects.create(
            name='Test Reward',
            description='Description de la récompense',
            points_cost=50
        )
        
        # Acheter la récompense
        self.user_reward = UserReward.objects.create(
            user=self.user,
            reward=self.reward_item
        )
    
    def test_reward_item_creation(self):
        """
        Teste la création d'un objet de récompense
        """
        self.assertEqual(self.reward_item.name, 'Test Reward')
        self.assertEqual(self.reward_item.points_cost, 50)
        self.assertTrue(self.reward_item.is_active)
    
    def test_user_reward_creation(self):
        """
        Teste l'achat d'une récompense par un utilisateur
        """
        self.assertEqual(self.user_reward.user, self.user)
        self.assertEqual(self.user_reward.reward, self.reward_item)


class ProgressViewTest(TestCase):
    """
    Tests pour les vues de progression
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
        
        # Créer un enregistrement de progression
        self.progress_record = ProgressRecord.objects.create(
            user=self.user,
            exercise_type=self.exercise_type,
            skill_level=3,
            exercises_completed=5
        )
    
    def test_progress_report_requires_login(self):
        """
        Teste que le rapport de progression nécessite une connexion
        """
        response = self.client.get(reverse('progress:progress_report'))
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
    
    def test_progress_report_logged_in(self):
        """
        Teste l'accès au rapport de progression lorsque l'utilisateur est connecté
        """
        self.client.login(username='test_user', password='password123')
        response = self.client.get(reverse('progress:progress_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'progress/progress_report.html')
        self.assertContains(response, 'Reconnaissance de lettres')
