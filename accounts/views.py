from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import json

from .models import ChildProfile, ParentProfile, TeacherProfile
from .forms import UserProfileForm, ChildProfileForm, ParentProfileForm, TeacherProfileForm, ChildUserForm

User = get_user_model()

@login_required
def profile_view(request):
    """
    Affiche et permet de modifier le profil de l'utilisateur connecté
    """
    user = request.user
    
    # Déterminer le type de profil
    if user.is_child:
        profile = getattr(user, 'child_profile', None)
        profile_form = ChildProfileForm(instance=profile)
    elif user.is_parent:
        profile = getattr(user, 'parent_profile', None)
        profile_form = ParentProfileForm(instance=profile)
    elif user.is_teacher:
        profile = getattr(user, 'teacher_profile', None)
        profile_form = TeacherProfileForm(instance=profile)
    else:
        profile = None
        profile_form = None
    
    user_form = UserProfileForm(instance=user)
    
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        
        if user.is_child:
            profile_form = ChildProfileForm(request.POST, instance=profile)
        elif user.is_parent:
            profile_form = ParentProfileForm(request.POST, instance=profile)
        elif user.is_teacher:
            profile_form = TeacherProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            
            if profile_form:
                profile_form.save()
            
            messages.success(request, _("Votre profil a été mis à jour avec succès."))
            return redirect('accounts:profile')
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile_type': user.user_type
    }
    
    return render(request, 'accounts/profile.html', context)

@login_required
@require_POST
def toggle_dyslexia_mode(request):
    """
    Active ou désactive le mode dyslexie pour un enfant
    """
    if not request.user.is_child:
        return JsonResponse({'status': 'error', 'message': _("Seuls les enfants peuvent activer le mode dyslexie.")})
    
    try:
        data = json.loads(request.body)
        dyslexia_mode = data.get('dyslexia_mode', False)
        
        profile = request.user.child_profile
        profile.dyslexia_mode = dyslexia_mode
        profile.save()
        
        return JsonResponse({'status': 'success', 'dyslexia_mode': dyslexia_mode})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
def children_list(request):
    """
    Affiche la liste des enfants d'un parent
    """
    if not request.user.is_parent:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    parent_profile = request.user.parent_profile
    children = parent_profile.children.all()
    
    context = {
        'children': children
    }
    
    return render(request, 'accounts/children_list.html', context)

@login_required
def add_child(request):
    """
    Permet à un parent d'ajouter un enfant
    """
    if not request.user.is_parent:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        user_form = ChildUserForm(request.POST)
        profile_form = ChildProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            # Créer l'utilisateur enfant
            user = user_form.save(commit=False)
            user.user_type = 'child'
            user.save()
            
            # Créer le profil enfant
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            # Associer l'enfant au parent
            parent_profile = request.user.parent_profile
            parent_profile.children.add(user)
            
            messages.success(request, _("L'enfant a été ajouté avec succès."))
            return redirect('accounts:children_list')
    else:
        user_form = ChildUserForm()
        profile_form = ChildProfileForm()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'accounts/add_child.html', context)

@login_required
def edit_child(request, child_id):
    """
    Permet à un parent de modifier un enfant
    """
    if not request.user.is_parent:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    parent_profile = request.user.parent_profile
    
    # Vérifier si l'enfant appartient au parent
    try:
        child = User.objects.get(id=child_id)
        if parent_profile not in child.parents.all():
            messages.error(request, _("Cet enfant n'est pas associé à votre compte."))
            return redirect('accounts:children_list')
    except User.DoesNotExist:
        messages.error(request, _("Cet enfant n'existe pas."))
        return redirect('accounts:children_list')
    
    child_profile = getattr(child, 'child_profile', None)
    if not child_profile:
        messages.error(request, _("Le profil de cet enfant est incomplet."))
        return redirect('accounts:children_list')
    
    if request.method == 'POST':
        user_form = ChildUserForm(request.POST, instance=child)
        profile_form = ChildProfileForm(request.POST, instance=child_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, _("Les informations de l'enfant ont été mises à jour avec succès."))
            return redirect('accounts:children_list')
    else:
        user_form = ChildUserForm(instance=child)
        profile_form = ChildProfileForm(instance=child_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'child': child
    }
    
    return render(request, 'accounts/edit_child.html', context)

# @login_required
# def edit_child(request, child_id):
#     """
#     Permet à un parent de modifier un enfant
#     """
#     if not request.user.is_parent:
#         messages.error(request, _("Vous n'avez pas accès à cette page."))
#         return redirect('dashboard:dashboard')
    
#     parent_profile = request.user.parent_profile
#     child = get_object_or_404(User, id=child_id, parents=parent_profile.user)
#     child_profile = child.child_profile
    
#     if request.method == 'POST':
#         user_form = ChildUserForm(request.POST, instance=child)
#         profile_form = ChildProfileForm(request.POST, instance=child_profile)
        
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
            
#             messages.success(request, _("Les informations de l'enfant ont été mises à jour avec succès."))
#             return redirect('accounts:children_list')
#     else:
#         user_form = ChildUserForm(instance=child)
#         profile_form = ChildProfileForm(instance=child_profile)
    
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'child': child
#     }
    
#     return render(request, 'accounts/edit_child.html', context)

@login_required
def students_list(request):
    """
    Affiche la liste des élèves d'un enseignant
    """
    if not request.user.is_teacher:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    teacher_profile = request.user.teacher_profile
    students = teacher_profile.students.all()
    
    context = {
        'students': students
    }
    
    return render(request, 'accounts/students_list.html', context)

@login_required
def add_student(request):
    """
    Permet à un enseignant d'ajouter un élève existant
    """
    if not request.user.is_teacher:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        
        try:
            student = User.objects.get(username=username, user_type='child')
            
            # Vérifier si l'élève est déjà associé à l'enseignant
            teacher_profile = request.user.teacher_profile
            if student in teacher_profile.students.all():
                messages.warning(request, _("Cet élève est déjà dans votre liste."))
            else:
                teacher_profile.students.add(student)
                messages.success(request, _("L'élève a été ajouté avec succès."))
            
            return redirect('accounts:students_list')
        except User.DoesNotExist:
            messages.error(request, _("Aucun élève trouvé avec ce nom d'utilisateur."))
    
    return render(request, 'accounts/add_student.html')

@login_required
def remove_student(request, student_id):
    """
    Permet à un enseignant de retirer un élève de sa liste
    """
    if not request.user.is_teacher:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    teacher_profile = request.user.teacher_profile
    student = get_object_or_404(User, id=student_id, teachers=request.user)
    
    teacher_profile.students.remove(student)
    messages.success(request, _("L'élève a été retiré de votre liste."))
    
    return redirect('accounts:students_list')

@login_required
def delete_child(request, child_id):
    """
    Permet à un parent de supprimer un enfant
    """
    if not request.user.is_parent:
        messages.error(request, _("Vous n'avez pas accès à cette page."))
        return redirect('dashboard:dashboard')
    
    parent_profile = request.user.parent_profile
    child = get_object_or_404(User, id=child_id, parents=parent_profile.user)
    
    if request.method == 'POST':
        # Supprimer l'association avec le parent
        parent_profile.children.remove(child)
        
        # Supprimer l'utilisateur et son profil
        child_username = child.username
        child.delete()
        
        messages.success(request, _(f"Le profil de {child_username} a été supprimé avec succès."))
        return redirect('accounts:children_list')
    
    context = {
        'child': child
    }
    
    return render(request, 'accounts/delete_child.html', context)