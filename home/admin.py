from django.contrib import admin
from .models import (Opportunity, Training, Application, Enrollment,
                     Profile, ContactMessage, Payment)


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
    list_display = ('title', 'duration', 'price', 'enrolled')

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
    list_display = ('full_name', 'training', 'email', 'phone', 'education', 'status', 'paid', 'enrolled_at')
    list_editable = ('status',)
    list_filter = ('status', 'training', 'education')
    search_fields = ('full_name', 'email')

    def paid(self, obj):
        return obj.is_paid
    paid.boolean = True  # shows a green tick or a red cross


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'enrollment', 'amount', 'phone', 'status', 'mpesa_receipt', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'phone', 'mpesa_receipt')
    # These come from Safaricom, so the admin can read them but not change them
    readonly_fields = ('merchant_request_id', 'checkout_request_id', 'mpesa_receipt',
                       'result_desc', 'created_at', 'updated_at')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    search_fields = ('name', 'email', 'message')