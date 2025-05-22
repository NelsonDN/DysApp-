from django.contrib import admin
from .models import Achievement, UserAchievement, ProgressRecord

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'points', 'icon')
    search_fields = ('name', 'description')
    list_filter = ('points',)

@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    list_display = ('user', 'achievement', 'date_earned')
    list_filter = ('achievement', 'date_earned')
    search_fields = ('user__username', 'achievement__name')
    date_hierarchy = 'date_earned'

@admin.register(ProgressRecord)
class ProgressRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'exercise_type', 'skill_level', 'exercises_completed', 'last_updated')
    list_filter = ('exercise_type', 'skill_level')
    search_fields = ('user__username', 'exercise_type__name')
    date_hierarchy = 'last_updated'

# from django.contrib import admin
# from .models import ProgressRecord, Achievement, UserAchievement, ProgressReport, RewardItem, UserReward

# admin.site.register(ProgressRecord)
# admin.site.register(Achievement)
# admin.site.register(UserAchievement)
# admin.site.register(ProgressReport)
# admin.site.register(RewardItem)
# admin.site.register(UserReward)