from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class ExerciseCategory(models.Model):
    """
    Catégorie d'exercices (ex: Lecture, Écriture, Nombres, Calcul, Problèmes)
    """
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    
    icon = models.CharField(
        max_length=50,
        default="fa-tasks",
        verbose_name=_("Icône")
    )
    
    color = models.CharField(
        max_length=20,
        default="#4E54C8",
        verbose_name=_("Couleur")
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
        verbose_name = _("Catégorie d'exercice")
        verbose_name_plural = _("Catégories d'exercices")
        ordering = ['name']
    
    def __str__(self):
        return self.name


class ExerciseType(models.Model):
    """
    Type d'exercice (ex: Reconnaissance de lettres, Lecture de mots, etc.)
    """
    DISORDER_TYPE_CHOICES = (
        ('dyslexia', 'Dyslexie'),
        ('dyscalculia', 'Dyscalculie'),
        ('both', 'Les deux'),
    )
    
    name = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    
    category = models.ForeignKey(
        ExerciseCategory,
        on_delete=models.CASCADE,
        related_name='exercise_types',
        verbose_name=_("Catégorie")
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_("Description")
    )
    
    disorder_type = models.CharField(
        max_length=20,
        choices=DISORDER_TYPE_CHOICES,
        default='both',
        verbose_name=_("Type de trouble")
    )
    
    icon = models.CharField(
        max_length=50,
        default="fa-tasks",
        verbose_name=_("Icône")
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
        verbose_name = _("Type d'exercice")
        verbose_name_plural = _("Types d'exercices")
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_disorder_type_display()})"


class Exercise(models.Model):
    """
    Exercice spécifique
    """
    DIFFICULTY_CHOICES = (
        (1, 'Facile'),
        (2, 'Moyen'),
        (3, 'Difficile'),
    )
    
    title = models.CharField(
        max_length=200,
        verbose_name=_("Titre")
    )
    
    exercise_type = models.ForeignKey(
        ExerciseType,
        on_delete=models.CASCADE,
        related_name='exercises',
        verbose_name=_("Type d'exercice")
    )
    
    instructions = models.TextField(
        verbose_name=_("Instructions")
    )
    
    difficulty = models.PositiveSmallIntegerField(
        choices=DIFFICULTY_CHOICES,
        default=1,
        verbose_name=_("Difficulté")
    )
    
    estimated_time = models.PositiveSmallIntegerField(
        default=10,
        verbose_name=_("Temps estimé (minutes)")
    )
    
    points = models.PositiveIntegerField(
        default=50,
        verbose_name=_("Points à gagner")
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
        verbose_name = _("Exercice")
        verbose_name_plural = _("Exercices")
        ordering = ['exercise_type', 'difficulty', 'title']
    
    def __str__(self):
        return self.title
    
    def get_difficulty_display_class(self):
        """
        Retourne la classe CSS pour la difficulté
        """
        if self.difficulty == 1:
            return 'success'
        elif self.difficulty == 2:
            return 'primary'
        else:
            return 'danger'


class Question(models.Model):
    """
    Question dans un exercice
    """
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Choix multiple'),
        ('true_false', 'Vrai ou faux'),
        ('matching', 'Association'),
        ('drag_drop', 'Glisser-déposer'),
        ('fill_blank', 'Texte à trous'),
        ('audio', 'Audio'),
        ('visual', 'Visuel'),
    )
    
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name=_("Exercice")
    )
    
    question_text = models.TextField(
        verbose_name=_("Texte de la question")
    )
    
    question_type = models.CharField(
        max_length=20,
        choices=QUESTION_TYPE_CHOICES,
        default='multiple_choice',
        verbose_name=_("Type de question")
    )
    
    image = models.ImageField(
        upload_to='questions/',
        blank=True,
        null=True,
        verbose_name=_("Image")
    )
    
    audio = models.FileField(
        upload_to='questions/audio/',
        blank=True,
        null=True,
        verbose_name=_("Audio")
    )
    
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Ordre")
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
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ['exercise', 'order']
    
    def __str__(self):
        return f"Question {self.order} - {self.exercise.title}"


class Answer(models.Model):
    """
    Réponse possible à une question
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name=_("Question")
    )
    
    answer_text = models.TextField(
        verbose_name=_("Texte de la réponse")
    )
    
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Est correcte")
    )
    
    feedback = models.TextField(
        blank=True,
        verbose_name=_("Feedback")
    )
    
    image = models.ImageField(
        upload_to='answers/',
        blank=True,
        null=True,
        verbose_name=_("Image")
    )
    
    order = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_("Ordre")
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
        verbose_name = _("Réponse")
        verbose_name_plural = _("Réponses")
        ordering = ['question', 'order']
    
    def __str__(self):
        return f"Réponse {self.order} - {self.question}"


class ExerciseAttempt(models.Model):
    """
    Tentative d'exercice par un utilisateur
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='exercise_attempts',
        verbose_name=_("Utilisateur")
    )
    
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name='attempts',
        verbose_name=_("Exercice")
    )
    
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de début")
    )
    
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Date de fin")
    )
    
    score = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Score")
    )
    
    max_score = models.PositiveIntegerField(
        default=100,
        verbose_name=_("Score maximum")
    )
    
    time_spent = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Temps passé (secondes)")
    )
    
    is_completed = models.BooleanField(
        default=False,
        verbose_name=_("Est terminé")
    )
    
    class Meta:
        verbose_name = _("Tentative d'exercice")
        verbose_name_plural = _("Tentatives d'exercices")
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.exercise.title}"
    
    @property
    def score_percentage(self):
        """
        Retourne le pourcentage de score
        """
        if self.max_score > 0:
            return (self.score / self.max_score) * 100
        return 0


class QuestionResponse(models.Model):
    """
    Réponse d'un utilisateur à une question
    """
    attempt = models.ForeignKey(
        ExerciseAttempt,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_("Tentative")
    )
    
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name=_("Question")
    )
    
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        related_name='responses',
        null=True,
        blank=True,
        verbose_name=_("Réponse")
    )
    
    text_response = models.TextField(
        blank=True,
        null=True,  # ← Ajoutez cette ligne
        default="",  # ← Ajoutez cette ligne aussi
        verbose_name=_("Réponse textuelle")
    )
    
    is_correct = models.BooleanField(
        default=False,
        verbose_name=_("Est correcte")
    )
    
    response_time = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Temps de réponse (secondes)")
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date de création")
    )
    
    class Meta:
        verbose_name = _("Réponse à une question")
        verbose_name_plural = _("Réponses aux questions")
        ordering = ['attempt', 'question']
    
    def __str__(self):
        return f"{self.attempt.user.username} - {self.question}"
