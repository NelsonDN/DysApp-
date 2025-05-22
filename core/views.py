from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from exercises.models import ExerciseCategory, Exercise

def home(request):
    """
    Page d'accueil du site
    """
    # Récupérer les catégories d'exercices
    categories = ExerciseCategory.objects.all()[:6]
    
    # Récupérer quelques exercices populaires
    popular_exercises = Exercise.objects.filter(is_active=True).order_by('-attempts__count')[:6]
    
    context = {
        'categories': categories,
        'popular_exercises': popular_exercises,
        'title': _('Accueil')
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """
    Page À propos
    """
    context = {
        'title': _('À propos')
    }
    
    return render(request, 'core/about.html', context)

def contact(request):
    """
    Page de contact
    """
    context = {
        'title': _('Contact')
    }
    
    return render(request, 'core/contact.html', context)

def privacy(request):
    """
    Politique de confidentialité
    """
    context = {
        'title': _('Politique de confidentialité')
    }
    
    return render(request, 'core/privacy.html', context)

def terms(request):
    """
    Conditions d'utilisation
    """
    context = {
        'title': _('Conditions d\'utilisation')
    }
    
    return render(request, 'core/terms.html', context)

@login_required
def dyslexia_info(request):
    """
    Page d'information sur la dyslexie
    """
    context = {
        'title': _('Comprendre la dyslexie')
    }
    
    return render(request, 'core/dyslexia_info.html', context)

@login_required
def dyscalculia_info(request):
    """
    Page d'information sur la dyscalculie
    """
    context = {
        'title': _('Comprendre la dyscalculie')
    }
    
    return render(request, 'core/dyscalculia_info.html', context)

@login_required
def resources(request):
    """
    Page de ressources pour les parents et enseignants
    """
    context = {
        'title': _('Ressources')
    }
    
    return render(request, 'core/resources.html', context)
