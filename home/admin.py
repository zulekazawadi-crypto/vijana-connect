from django.contrib import admin
from .models import Opportunity, Training, Application, Enrollment


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    # "applicants" is a custom column showing how many people applied
    list_display = ('title', 'company', 'category', 'deadline', 'is_active', 'applicants')
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
    # "status" can be changed directly in the list (list_editable below)
    list_display = ('full_name', 'opportunity', 'email', 'phone', 'education', 'status', 'applied_at')
    list_editable = ('status',)
    list_filter = ('status', 'opportunity', 'education')
    search_fields = ('full_name', 'email')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    # "status" can be changed directly in the list (list_editable below)
    list_display = ('full_name', 'training', 'email', 'phone', 'education', 'status', 'enrolled_at')
    list_editable = ('status',)
    list_filter = ('status', 'training', 'education')
    search_fields = ('full_name', 'email')