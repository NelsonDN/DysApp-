from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import ChildProfile, ParentProfile, TeacherProfile

User = get_user_model()

class UserModelTest(TestCase):
    """
    Tests pour le modèle utilisateur personnalisé
    """
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='password123',
            user_type='admin'
        )
        
        self.parent_user = User.objects.create_user(
            username='parent_test',
            email='parent@test.com',
            password='password123',
            user_type='parent'
        )
        
        self.teacher_user = User.objects.create_user(
            username='teacher_test',
            email='teacher@test.com',
            password='password123',
            user_type='teacher'
        )
        
        self.child_user = User.objects.create_user(
            username='child_test',
            email='child@test.com',
            password='password123',
            user_type='child'
        )
    
    def test_user_creation(self):
        """
        Teste la création d'utilisateurs
        """
        self.assertEqual(self.admin_user.username, 'admin_test')
        self.assertEqual(self.parent_user.username, 'parent_test')
        self.assertEqual(self.teacher_user.username, 'teacher_test')
        self.assertEqual(self.child_user.username, 'child_test')
    
    def test_user_type_properties(self):
        """
        Teste les propriétés de type d'utilisateur
        """
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.admin_user.is_parent)
        self.assertFalse(self.admin_user.is_teacher)
        self.assertFalse(self.admin_user.is_child)
        
        self.assertTrue(self.parent_user.is_parent)
        self.assertFalse(self.parent_user.is_admin)
        self.assertFalse(self.parent_user.is_teacher)
        self.assertFalse(self.parent_user.is_child)
        
        self.assertTrue(self.teacher_user.is_teacher)
        self.assertFalse(self.teacher_user.is_admin)
        self.assertFalse(self.teacher_user.is_parent)
        self.assertFalse(self.teacher_user.is_child)
        
        self.assertTrue(self.child_user.is_child)
        self.assertFalse(self.child_user.is_admin)
        self.assertFalse(self.child_user.is_parent)
        self.assertFalse(self.child_user.is_teacher)


class ChildProfileTest(TestCase):
    """
    Tests pour le modèle ChildProfile
    """
    def setUp(self):
        self.child_user = User.objects.create_user(
            username='child_test',
            email='child@test.com',
            password='password123',
            user_type='child'
        )
        
        self.child_profile = ChildProfile.objects.create(
            user=self.child_user,
            school_level='ce2',
            has_dyslexia=True,
            dyslexia_level=2,
            has_dyscalculia=False,
            dyscalculia_level=None,
            points=150,
            level=1
        )
    
    def test_profile_creation(self):
        """
        Teste la création d'un profil enfant
        """
        self.assertEqual(self.child_profile.user, self.child_user)
        self.assertEqual(self.child_profile.school_level, 'ce2')
        self.assertTrue(self.child_profile.has_dyslexia)
        self.assertEqual(self.child_profile.dyslexia_level, 2)
        self.assertFalse(self.child_profile.has_dyscalculia)
        self.assertIsNone(self.child_profile.dyscalculia_level)
        self.assertEqual(self.child_profile.points, 150)
        self.assertEqual(self.child_profile.level, 1)
    
    def test_update_level(self):
        """
        Teste la mise à jour du niveau en fonction des points
        """
        # Niveau 1: 0-100 points
        self.child_profile.points = 50
        self.child_profile.update_level()
        self.assertEqual(self.child_profile.level, 1)
        
        # Niveau 2: 101-300 points
        self.child_profile.points = 200
        self.child_profile.update_level()
        self.assertEqual(self.child_profile.level, 2)
        
        # Niveau 3: 301-600 points
        self.child_profile.points = 500
        self.child_profile.update_level()
        self.assertEqual(self.child_profile.level, 3)


class ParentProfileTest(TestCase):
    """
    Tests pour le modèle ParentProfile
    """
    def setUp(self):
        self.parent_user = User.objects.create_user(
            username='parent_test',
            email='parent@test.com',
            password='password123',
            user_type='parent'
        )
        
        self.child_user1 = User.objects.create_user(
            username='child_test1',
            email='child1@test.com',
            password='password123',
            user_type='child'
        )
        
        self.child_user2 = User.objects.create_user(
            username='child_test2',
            email='child2@test.com',
            password='password123',
            user_type='child'
        )
        
        self.parent_profile = ParentProfile.objects.create(
            user=self.parent_user,
            phone_number='0123456789'
        )
        
        self.parent_profile.children.add(self.child_user1, self.child_user2)
    
    def test_profile_creation(self):
        """
        Teste la création d'un profil parent
        """
        self.assertEqual(self.parent_profile.user, self.parent_user)
        self.assertEqual(self.parent_profile.phone_number, '0123456789')
    
    def test_children_association(self):
        """
        Teste l'association des enfants au parent
        """
        self.assertEqual(self.parent_profile.children.count(), 2)
        self.assertIn(self.child_user1, self.parent_profile.children.all())
        self.assertIn(self.child_user2, self.parent_profile.children.all())


class TeacherProfileTest(TestCase):
    """
    Tests pour le modèle TeacherProfile
    """
    def setUp(self):
        self.teacher_user = User.objects.create_user(
            username='teacher_test',
            email='teacher@test.com',
            password='password123',
            user_type='teacher'
        )
        
        self.student1 = User.objects.create_user(
            username='student_test1',
            email='student1@test.com',
            password='password123',
            user_type='child'
        )
        
        self.student2 = User.objects.create_user(
            username='student_test2',
            email='student2@test.com',
            password='password123',
            user_type='child'
        )
        
        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher_user,
            school_name='École Test',
            specialization='Troubles DYS'
        )
        
        self.teacher_profile.students.add(self.student1, self.student2)
    
    def test_profile_creation(self):
        """
        Teste la création d'un profil enseignant
        """
        self.assertEqual(self.teacher_profile.user, self.teacher_user)
        self.assertEqual(self.teacher_profile.school_name, 'École Test')
        self.assertEqual(self.teacher_profile.specialization, 'Troubles DYS')
    
    def test_students_association(self):
        """
        Teste l'association des élèves à l'enseignant
        """
        self.assertEqual(self.teacher_profile.students.count(), 2)
        self.assertIn(self.student1, self.teacher_profile.students.all())
        self.assertIn(self.student2, self.teacher_profile.students.all())


class ProfileViewTest(TestCase):
    """
    Tests pour la vue de profil
    """
    def setUp(self):
        self.client = Client()
        
        self.child_user = User.objects.create_user(
            username='child_test',
            email='child@test.com',
            password='password123',
            user_type='child'
        )
        
        self.child_profile = ChildProfile.objects.create(
            user=self.child_user,
            school_level='ce2',
            has_dyslexia=True,
            dyslexia_level=2,
            has_dyscalculia=False,
            dyscalculia_level=None
        )
    
    def test_profile_view_requires_login(self):
        """
        Teste que la vue de profil nécessite une connexion
        """
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirection vers la page de connexion
    
    def test_profile_view_logged_in(self):
        """
        Teste l'accès à la vue de profil lorsque l'utilisateur est connecté
        """
        self.client.login(username='child_test', password='password123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, 'child_test')
