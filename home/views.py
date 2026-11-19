from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Opportunity, Training, Application, Enrollment
from .forms import RegisterForm, ApplicationForm, EnrollmentForm


def index(request):
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')


def opportunities(request):
    # Read all active opportunities from the database and send them to the page
    items = Opportunity.objects.filter(is_active=True)
    return render(request, 'home/opportunities.html', {'items': items})


def training(request):
    courses = Training.objects.all()
    return render(request, 'home/training.html', {'courses': courses})


def register(request):
    """Create a new account, then log the person in."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Your account has been created.')
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'home/register.html', {'form': form})


@login_required  # sends people to the login page first if they are not logged in
def apply(request, opp_id):
    """Application form for one opportunity."""
    opportunity = get_object_or_404(Opportunity, id=opp_id)

    # Stop double applications
    if Application.objects.filter(user=request.user, opportunity=opportunity).exists():
        messages.info(request, 'You have already applied for this opportunity.')
        return redirect('opportunities')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)  # build it but do not save yet
            application.user = request.user        # who applied
            application.opportunity = opportunity  # what they applied for
            application.save()                     # now save to the database
            messages.success(request, 'Your application has been submitted.')
            return redirect('my_applications')
    else:
        form = ApplicationForm(initial={'email': request.user.email})

    return render(request, 'home/details_form.html', {
        'form': form,
        'page_title': 'Apply',
        'heading': f'Apply: {opportunity.title}',
        'subheading': opportunity.company,
        'button_text': 'Submit Application',
    })


@login_required
def enroll(request, course_id):
    """Enrollment form for one training course."""
    course = get_object_or_404(Training, id=course_id)

    if Enrollment.objects.filter(user=request.user, training=course).exists():
        messages.info(request, 'You are already enrolled in this course.')
        return redirect('training')

    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.user = request.user
            enrollment.training = course
            enrollment.save()
            messages.success(request, 'You have been enrolled successfully.')
            return redirect('my_enrollments')
    else:
        form = EnrollmentForm(initial={'email': request.user.email})

    return render(request, 'home/details_form.html', {
        'form': form,
        'page_title': 'Enroll',
        'heading': f'Enroll: {course.title}',
        'subheading': f'Duration: {course.duration}',
        'button_text': 'Enroll Now',
    })


@login_required  # not logged in -> sent to the login page
def dashboard(request):
    """Shows how many people registered, applied and enrolled. Admin only."""

    # Logged in but not an admin -> send them home with a message
    if not request.user.is_staff:
        messages.warning(request, 'Only the admin can view the dashboard.')
        return redirect('index')

    context = {
        'total_users': User.objects.count(),
        'total_applications': Application.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        # Count() adds a "num" to each opportunity/course = how many applied/enrolled
        'opportunities': Opportunity.objects.annotate(num=Count('applications')).order_by('-num'),
        'courses': Training.objects.annotate(num=Count('enrollments')).order_by('-num'),
        'recent_applications': Application.objects.select_related('user', 'opportunity')[:10],
    }
    return render(request, 'home/dashboard.html', context)


@login_required
def my_applications(request):
    """Lets a logged-in user track the status of their own applications."""
    applications = Application.objects.filter(user=request.user).select_related('opportunity')
    return render(request, 'home/my_applications.html', {'applications': applications})


@login_required
def my_enrollments(request):
    """Lets a logged-in user track the status of their own training enrollments."""
    enrollments = Enrollment.objects.filter(user=request.user).select_related('training')
    return render(request, 'home/my_enrollments.html', {'enrollments': enrollments})