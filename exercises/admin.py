from django.contrib import admin
from .models import ExerciseCategory, ExerciseType, Exercise, Question, Answer, ExerciseAttempt, QuestionResponse

@admin.register(ExerciseCategory)
class ExerciseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'icon')
    search_fields = ('name', 'description')

@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'disorder_type', 'description')
    list_filter = ('disorder_type', 'category')
    search_fields = ('name', 'description')

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    fields = ('answer_text', 'is_correct', 'feedback', 'image', 'order')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'exercise', 'question_type', 'order')
    list_filter = ('question_type', 'exercise__exercise_type')
    search_fields = ('question_text', 'exercise__title')
    inlines = [AnswerInline]

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    show_change_link = True

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('title', 'exercise_type', 'difficulty', 'estimated_time', 'is_active')
    list_filter = ('exercise_type', 'difficulty', 'is_active')
    search_fields = ('title', 'instructions')
    inlines = [QuestionInline]

class QuestionResponseInline(admin.TabularInline):
    model = QuestionResponse
    extra = 0
    readonly_fields = ('question', 'answer', 'text_response', 'is_correct', 'response_time')

@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise', 'started_at', 'completed_at', 'score', 'is_completed')
    list_filter = ('is_completed', 'exercise__exercise_type')
    search_fields = ('user__username', 'exercise__title')
    readonly_fields = ('user', 'exercise', 'started_at', 'completed_at', 'score', 'max_score')
    inlines = [QuestionResponseInline]

@admin.register(QuestionResponse)
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('attempt', 'question', 'is_correct', 'response_time')
    list_filter = ('is_correct',)
    search_fields = ('attempt__user__username', 'question__question_text')
    readonly_fields = ('attempt', 'question', 'answer', 'text_response', 'is_correct', 'response_time')
