from django.db import models
from django.contrib.auth.models import User

# Choices shown in the "education" dropdown on the forms
EDUCATION_CHOICES = [
    ('KCSE', 'KCSE'),
    ('Certificate', 'Certificate'),
    ('Diploma', 'Diploma'),
    ('Degree', 'Degree'),
    ('Other', 'Other'),
]


class Opportunity(models.Model):
    """A job, vacancy or attachment posted by a company."""
    CATEGORY_CHOICES = [
        ('job', 'Job'),
        ('vacancy', 'Vacancy'),
        ('attachment', 'Attachment'),
    ]
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=50)
    description = models.TextField()
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.company}"


class Training(models.Model):
    """A training course people can enroll in."""
    title = models.CharField(max_length=150)
    description = models.TextField()
    duration = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Application(models.Model):
    """One person applying for one opportunity."""

    # The three results an application can have (the admin changes this)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('selected', 'Selected'),
        ('not_selected', 'Not Selected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE,
                                    related_name='applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES,
                                 verbose_name="Highest education level")
    message = models.TextField(blank=True, verbose_name="Why are you a good fit? (optional)")
    applied_at = models.DateTimeField(auto_now_add=True)

    # NEW: the result of the application, starts as "pending"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # NEW: the admin writes instructions here for people who are selected
    instructions = models.TextField(
        blank=True,
        help_text="Shown to the applicant when the status is Selected."
    )

    class Meta:
        # a person can apply to the same opportunity only once
        unique_together = ('user', 'opportunity')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} applied for {self.opportunity.title}"


class Enrollment(models.Model):
    """One person enrolling in one training course."""

    # The three results an enrollment can have (the admin changes this)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Not Accepted'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE,
                                 related_name='enrollments')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES,
                                 verbose_name="Highest education level")
    enrolled_at = models.DateTimeField(auto_now_add=True)

    # NEW: the result of the enrollment, starts as "pending"
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # NEW: the admin writes course details here (start date, venue, what to bring)
    instructions = models.TextField(
        blank=True,
        help_text="Shown to the learner when the status is Approved."
    )

    class Meta:
        unique_together = ('user', 'training')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.full_name} enrolled in {self.training.title}"