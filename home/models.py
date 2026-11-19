from django.db import models
from django.contrib.auth.models import User

# Education levels shown in the dropdowns
EDUCATION_CHOICES = [
    ('KCSE', 'KCSE'),
    ('Certificate', 'Certificate'),
    ('Diploma', 'Diploma'),
    ('Degree', 'Degree'),
    ('Other', 'Other'),
]

# Used to compare levels. "Other" ranks lowest, so it never meets a minimum.
EDUCATION_RANK = {'Other': 0, 'KCSE': 1, 'Certificate': 2, 'Diploma': 3, 'Degree': 4}


class Profile(models.Model):
    """Details a user fills in once, then reuses on every form."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    education = models.CharField(max_length=50, choices=EDUCATION_CHOICES,
                                 verbose_name="Highest education level")

    def __str__(self):
        return f"Profile of {self.user.username}"


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

    # NEW: requirements shown on the card and checked when someone applies
    min_education = models.CharField(
        max_length=50, choices=EDUCATION_CHOICES, blank=True,
        help_text="Leave empty if there is no minimum education."
    )
    requirements = models.TextField(
        blank=True,
        help_text="Other requirements, for example: 2 years experience, driving licence."
    )

    def is_met_by(self, education):
        """True if the given education level meets this opportunity's minimum."""
        if not self.min_education:
            return True
        return EDUCATION_RANK.get(education, 0) >= EDUCATION_RANK[self.min_education]

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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    instructions = models.TextField(
        blank=True,
        help_text="Shown to the applicant when the status is Selected."
    )

    class Meta:
        unique_together = ('user', 'opportunity')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} applied for {self.opportunity.title}"


class Enrollment(models.Model):
    """One person enrolling in one training course."""
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    instructions = models.TextField(
        blank=True,
        help_text="Shown to the learner when the status is Approved."
    )

    class Meta:
        unique_together = ('user', 'training')
        ordering = ['-enrolled_at']

    def __str__(self):
        return f"{self.full_name} enrolled in {self.training.title}"