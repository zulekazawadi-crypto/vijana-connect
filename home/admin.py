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
    # "enrolled" shows how many people enrolled in the course
    list_display = ('title', 'duration', 'enrolled')

    def enrolled(self, obj):
        return obj.enrollments.count()


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'opportunity', 'email', 'phone', 'education', 'applied_at')
    list_filter = ('opportunity', 'education')
    search_fields = ('full_name', 'email')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'training', 'email', 'phone', 'education', 'enrolled_at')
    list_filter = ('training', 'education')
    search_fields = ('full_name', 'email')