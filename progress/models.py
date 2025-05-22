from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from exercises.models import ExerciseType

class Achievement(models.Model):
    """
    Récompense que les utilisateurs peuvent gagner
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    
    description = models.TextField(
        verbose_name=_("Description")
    )
    
    icon = models.CharField(
        max_length=50,
        default="fa-trophy",
        verbose_name=_("Icône")
    )
    
    points = models.PositiveIntegerField(
        default=10,
        verbose_name=_("Points")
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
        verbose_name = _("Récompense")
        verbose_name_plural = _("Récompenses")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class UserAchievement(models.Model):
    """
    Récompense gagnée par un utilisateur
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements',
        verbose_name=_("Utilisateur")
    )
    
    achievement = models.ForeignKey(
        Achievement,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_("Récompense")
    )
    
    date_earned = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'obtention")
    )
    
    class Meta:
        verbose_name = _("Récompense utilisateur")
        verbose_name_plural = _("Récompenses utilisateurs")
        ordering = ['-date_earned']
        unique_together = ['user', 'achievement']
    
    def __str__(self):
        return f"{self.user.username} - {self.achievement.name}"


class ProgressRecord(models.Model):
    """
    Enregistrement de la progression d'un utilisateur pour un type d'exercice
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name=_("Utilisateur")
    )
    
    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.CASCADE,
        related_name='progress_records',
        verbose_name=_("Type d'exercice")
    )
    
    skill_level = models.PositiveSmallIntegerField(
        default=1,
        verbose_name=_("Niveau de compétence")
    )
    
    exercises_completed = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Exercices complétés")
    )
    
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Dernière mise à jour")
    )
    
    class Meta:
        verbose_name = _("Enregistrement de progression")
        verbose_name_plural = _("Enregistrements de progression")
        ordering = ['user', 'exercise_type']
        unique_together = ['user', 'exercise_type']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise_type.name}"


class ProgressReport(models.Model):
    """
    Rapport de progression généré périodiquement
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='progress_reports',
        verbose_name=_("Utilisateur")
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_("Titre")
    )
    
    content = models.TextField(
        verbose_name=_("Contenu")
    )
    
    period_start = models.DateField(
        verbose_name=_("Début de période")
    )
    
    period_end = models.DateField(
        verbose_name=_("Fin de période")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    class Meta:
        verbose_name = _("Rapport de progression")
        verbose_name_plural = _("Rapports de progression")
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"


class RewardItem(models.Model):
    """
    Objet de récompense que les utilisateurs peuvent acheter avec leurs points
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    
    description = models.TextField(
        verbose_name=_("Description")
    )
    
    image = models.ImageField(
        upload_to='rewards/',
        blank=True,
        null=True,
        verbose_name=_("Image")
    )
    
    points_cost = models.PositiveIntegerField(
        default=50,
        verbose_name=_("Coût en points")
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
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
        verbose_name = _("Objet de récompense")
        verbose_name_plural = _("Objets de récompense")
        ordering = ['points_cost', 'name']
    
    def __str__(self):
        return self.name


class UserReward(models.Model):
    """
    Objet de récompense acheté par un utilisateur
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='rewards',
        verbose_name=_("Utilisateur")
    )
    
    reward = models.ForeignKey(
        RewardItem,
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name=_("Récompense")
    )
    
    date_acquired = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'acquisition")
    )
    
    class Meta:
        verbose_name = _("Récompense utilisateur")
        verbose_name_plural = _("Récompenses utilisateurs")
        ordering = ['-date_acquired']
    
    def __str__(self):
        return f"{self.user.username} - {self.reward.name}"
