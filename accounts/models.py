from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Modèle utilisateur personnalisé avec un champ pour le type d'utilisateur
    """
    USER_TYPE_CHOICES = (
        ('admin', 'Administrateur'),
        ('teacher', 'Enseignant'),
        ('parent', 'Parent'),
        ('child', 'Enfant'),
    )
    
    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='child',
        verbose_name=_("Type d'utilisateur")
    )
    
    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
    
    def __str__(self):
        return self.username
    
    @property
    def is_child(self):
        return self.user_type == 'child'
    
    @property
    def is_parent(self):
        return self.user_type == 'parent'
    
    @property
    def is_teacher(self):
        return self.user_type == 'teacher'
    
    @property
    def is_admin(self):
        return self.user_type == 'admin'


class ChildProfile(models.Model):
    """
    Profil pour les utilisateurs de type enfant
    """
    SCHOOL_LEVEL_CHOICES = (
        ('cp', 'CP'),
        ('ce1', 'CE1'),
        ('ce2', 'CE2'),
        ('cm1', 'CM1'),
        ('cm2', 'CM2'),
        ('6eme', '6ème'),
        ('5eme', '5ème'),
        ('4eme', '4ème'),
        ('3eme', '3ème'),
    )
    
    DYSLEXIA_LEVEL_CHOICES = (
        (1, 'Légère'),
        (2, 'Modérée'),
        (3, 'Sévère'),
    )
    
    DYSCALCULIA_LEVEL_CHOICES = (
        (1, 'Légère'),
        (2, 'Modérée'),
        (3, 'Sévère'),
    )
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='child_profile',
        verbose_name=_("Utilisateur")
    )
    
    school_level = models.CharField(
        max_length=5,
        choices=SCHOOL_LEVEL_CHOICES,
        verbose_name=_("Niveau scolaire")
    )
    
    has_dyslexia = models.BooleanField(
        default=False,
        verbose_name=_("A de la dyslexie")
    )
    
    dyslexia_level = models.PositiveSmallIntegerField(
        choices=DYSLEXIA_LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Niveau de dyslexie")
    )
    
    has_dyscalculia = models.BooleanField(
        default=False,
        verbose_name=_("A de la dyscalculie")
    )
    
    dyscalculia_level = models.PositiveSmallIntegerField(
        choices=DYSCALCULIA_LEVEL_CHOICES,
        null=True,
        blank=True,
        verbose_name=_("Niveau de dyscalculie")
    )
    
    points = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Points")
    )
    
    level = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Niveau")
    )
    
    dyslexia_mode = models.BooleanField(
        default=False,
        verbose_name=_("Mode dyslexie activé")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )
    
    class Meta:
        verbose_name = _("Profil enfant")
        verbose_name_plural = _("Profils enfants")
    
    def __str__(self):
        return f"Profil de {self.user.username}"
    
    def update_level(self):
        """
        Met à jour le niveau de l'enfant en fonction de ses points
        """
        # Chaque niveau nécessite 100 points de plus que le précédent
        points_needed = 0
        for level in range(1, 11):  # Max level is 10
            points_needed += level * 100
            if self.points < points_needed:
                self.level = level
                break
        self.save()


class ParentProfile(models.Model):
    """
    Profil pour les utilisateurs de type parent
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='parent_profile',
        verbose_name=_("Utilisateur")
    )
    
    children = models.ManyToManyField(
        User,
        related_name='parents',
        blank=True,
        verbose_name=_("Enfants")
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_("Numéro de téléphone")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )
    
    class Meta:
        verbose_name = _("Profil parent")
        verbose_name_plural = _("Profils parents")
    
    def __str__(self):
        return f"Profil de {self.user.username}"


class TeacherProfile(models.Model):
    """
    Profil pour les utilisateurs de type enseignant
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name=_("Utilisateur")
    )
    
    students = models.ManyToManyField(
        User,
        related_name='teachers',
        blank=True,
        verbose_name=_("Élèves")
    )
    
    school_name = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Nom de l'école")
    )
    
    specialization = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Spécialisation")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Date de mise à jour")
    )
    
    class Meta:
        verbose_name = _("Profil enseignant")
        verbose_name_plural = _("Profils enseignants")
    
    def __str__(self):
        return f"Profil de {self.user.username}"
