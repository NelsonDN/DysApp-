from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import ChildProfile, ParentProfile, TeacherProfile

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_active', 'date_joined')
    list_filter = ('user_type', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informations personnelles', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'user_type', 'groups', 'user_permissions')}),
        ('Dates importantes', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(ChildProfile)
class ChildProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_level', 'has_dyslexia', 'has_dyscalculia', 'points', 'level')
    list_filter = ('school_level', 'has_dyslexia', 'has_dyscalculia')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')

@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_children_count')
    search_fields = ('user__username', 'user__first_name', 'user__last_name')
    filter_horizontal = ('children',)
    
    def get_children_count(self, obj):
        return obj.children.count()
    get_children_count.short_description = 'Nombre d\'enfants'

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'school_name', 'get_students_count')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'school_name')
    filter_horizontal = ('students',)
    
    def get_students_count(self, obj):
        return obj.students.count()
    get_students_count.short_description = 'Nombre d\'élèves'

# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from .models import User, ChildProfile, ParentProfile, TeacherProfile

# admin.site.register(User, UserAdmin)
# admin.site.register(ChildProfile)
# admin.site.register(ParentProfile)
# admin.site.register(TeacherProfile)