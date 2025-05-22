from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Exercise, Question, Answer

class ExerciseForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier un exercice
    """
    class Meta:
        model = Exercise
        fields = ['title', 'exercise_type', 'instructions', 'difficulty', 'estimated_time', 'points', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'exercise_type': forms.Select(attrs={'class': 'form-select'}),
            'instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'estimated_time': forms.NumberInput(attrs={'class': 'form-control'}),
            'points': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }


class QuestionForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une question
    """
    class Meta:
        model = Question
        fields = ['question_text', 'question_type', 'image', 'audio', 'order']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'audio': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }


class AnswerForm(forms.ModelForm):
    """
    Formulaire pour créer ou modifier une réponse
    """
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct', 'feedback', 'image', 'order']
        widgets = {
            'answer_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'})
        }


class AnswerInlineFormSet(forms.BaseInlineFormSet):
    """
    FormSet pour gérer plusieurs réponses à une question
    """
    def clean(self):
        super().clean()
        
        # Vérifier qu'au moins une réponse est correcte
        has_correct_answer = False
        
        for form in self.forms:
            if not form.is_valid() or form.cleaned_data.get('DELETE'):
                continue
            
            if form.cleaned_data.get('is_correct'):
                has_correct_answer = True
                break
        
        if not has_correct_answer:
            raise forms.ValidationError(_("Au moins une réponse doit être correcte."))
