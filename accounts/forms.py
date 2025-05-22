from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from .models import ChildProfile, ParentProfile, TeacherProfile

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier les informations de base d'un utilisateur
    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }


class ChildProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier le profil d'un enfant
    """
    class Meta:
        model = ChildProfile
        fields = ['school_level', 'has_dyslexia', 'dyslexia_level', 'has_dyscalculia', 'dyscalculia_level']
        widgets = {
            'school_level': forms.Select(attrs={'class': 'form-select'}),
            'has_dyslexia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dyslexia_level': forms.Select(attrs={'class': 'form-select'}),
            'has_dyscalculia': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dyscalculia_level': forms.Select(attrs={'class': 'form-select'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dyslexia_level'].required = False
        self.fields['dyscalculia_level'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        has_dyslexia = cleaned_data.get('has_dyslexia')
        dyslexia_level = cleaned_data.get('dyslexia_level')
        has_dyscalculia = cleaned_data.get('has_dyscalculia')
        dyscalculia_level = cleaned_data.get('dyscalculia_level')
        
        if has_dyslexia and not dyslexia_level:
            self.add_error('dyslexia_level', _("Ce champ est obligatoire si l'enfant a de la dyslexie."))
        
        if has_dyscalculia and not dyscalculia_level:
            self.add_error('dyscalculia_level', _("Ce champ est obligatoire si l'enfant a de la dyscalculie."))
        
        return cleaned_data


class ParentProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier le profil d'un parent
    """
    class Meta:
        model = ParentProfile
        fields = ['phone_number']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'})
        }


class TeacherProfileForm(forms.ModelForm):
    """
    Formulaire pour modifier le profil d'un enseignant
    """
    class Meta:
        model = TeacherProfile
        fields = ['school_name', 'specialization']
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'})
        }


class ChildUserForm(forms.ModelForm):
    """
    Formulaire pour créer un utilisateur enfant
    """
    password1 = forms.CharField(
        label=_("Mot de passe"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )
    
    password2 = forms.CharField(
        label=_("Confirmation du mot de passe"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        strip=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(_("Les mots de passe ne correspondent pas."))
        
        return password2
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        
        return user
