from django.contrib import admin
from .models import Opportunity, Training, Application, Enrollment, Profile, ContactMessage


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'education')
    search_fields = ('full_name', 'user__username')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'min_education', 'deadline', 'is_active', 'applicants')
    list_filter = ('category', 'is_active')

    def applicants(self, obj):
        return obj.applications.count()


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'duration', 'enrolled')

    def enrolled(self, obj):
        return obj.enrollments.count()


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'opportunity', 'email', 'phone', 'education', 'status', 'applied_at')
    list_editable = ('status',)
    list_filter = ('status', 'opportunity', 'education')
    search_fields = ('full_name', 'email')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'training', 'email', 'phone', 'education', 'status', 'enrolled_at')
    list_editable = ('status',)
    list_filter = ('status', 'training', 'education')
    search_fields = ('full_name', 'email')

    @admin.register(ContactMessage)
    class ContactMessageAdmin(admin.ModelAdmin):
        list_display = ('name', 'email', 'created_at')
        search_fields = ('name', 'email', 'message')