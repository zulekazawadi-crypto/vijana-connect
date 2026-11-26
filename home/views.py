import json

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Opportunity, Training, Application, Enrollment, Profile, ContactMessage, Payment
from .forms import RegisterForm, ProfileForm, ApplicationForm, EnrollmentForm
from .mpesa import stk_push, stk_query, format_phone, MpesaError

def index(request):
    # Latest active opportunities, split by category, for the homepage tabs
    active = Opportunity.objects.filter(is_active=True).order_by('-id')
    context = {
        'jobs': active.filter(category='job')[:5],
        'vacancies': active.filter(category='vacancy')[:5],
        'attachments': active.filter(category='attachment')[:5],
        'job_count': active.filter(category='job').count(),
        'vacancy_count': active.filter(category='vacancy').count(),
        'attachment_count': active.filter(category='attachment').count(),
        'course_count': Training.objects.count(),
    }
    return render(request, 'home/index.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    """Show the contact page. When the form is sent, save the message to the database."""
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', '').strip()[:100],
            email=request.POST.get('email', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Thank you! Your message has been sent.')
        return redirect('contact')
    return render(request, 'home/contact.html')


def opportunities(request):
    items = Opportunity.objects.filter(is_active=True)
    return render(request, 'home/opportunities.html', {'items': items})


def training(request):
    courses = Training.objects.all()
    return render(request, 'home/training.html', {'courses': courses})


def register(request):
    """Create a new account, log the person in, then ask them to complete their profile."""
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome! Please complete your profile.')
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'home/register.html', {'form': form})


@login_required
def profile(request):
    """Create or edit the logged-in user's profile."""
    existing = Profile.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=existing)
        if form.is_valid():
            saved = form.save(commit=False)
            saved.user = request.user
            saved.save()
            messages.success(request, 'Your profile has been saved.')
            return redirect('opportunities')
    else:
        form = ProfileForm(instance=existing)

    return render(request, 'home/details_form.html', {
        'form': form,
        'page_title': 'My Profile',
        'heading': 'My Profile',
        'subheading': 'Fill this in once and we will use it on your applications.',
        'button_text': 'Save Profile',
    })


@login_required
def apply(request, opp_id):
    """Application form for one opportunity."""
    opportunity = get_object_or_404(Opportunity, id=opp_id)

    # Step 1: the person must have a profile first
    user_profile = Profile.objects.filter(user=request.user).first()
    if user_profile is None:
        messages.info(request, 'Please complete your profile before applying.')
        return redirect('profile')

    # Step 2: Meets Requirements? If not, send them back to Explore Opportunities
    if not opportunity.is_met_by(user_profile.education):
        messages.warning(
            request,
            f'Sorry, you do not meet the requirements for {opportunity.title}. '
            f'Minimum education: {opportunity.get_min_education_display()}. '
            f'Explore the other opportunities below.'
        )
        return redirect('opportunities')

    # Step 3: stop double applications
    if Application.objects.filter(user=request.user, opportunity=opportunity).exists():
        messages.info(request, 'You have already applied for this opportunity.')
        return redirect('opportunities')

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.opportunity = opportunity
            application.save()
            messages.success(request, 'Your application has been submitted.')
            return redirect('my_applications')
    else:
        form = ApplicationForm(initial={
            'full_name': user_profile.full_name,
            'email': request.user.email,
            'phone': user_profile.phone,
            'education': user_profile.education,
        })

    return render(request, 'home/details_form.html', {
        'form': form,
        'page_title': 'Apply',
        'heading': f'Apply: {opportunity.title}',
        'subheading': opportunity.company,
        'button_text': 'Submit Application',
    })


@login_required
def enroll(request, course_id):
    """Enrollment form for one training course. Paid courses go on to the payment page."""
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

            if course.price > 0:
                messages.info(request, 'You are enrolled. Please pay the course fee to complete it.')
                return redirect('pay', enrollment_id=enrollment.id)

            messages.success(request, 'You have been enrolled successfully.')
            return redirect('my_enrollments')
    else:
        user_profile = Profile.objects.filter(user=request.user).first()
        initial = {'email': request.user.email}
        if user_profile:
            initial.update({
                'full_name': user_profile.full_name,
                'phone': user_profile.phone,
                'education': user_profile.education,
            })
        form = EnrollmentForm(initial=initial)

    return render(request, 'home/details_form.html', {
        'form': form,
        'page_title': 'Enroll',
        'heading': f'Enroll: {course.title}',
        'subheading': f'Duration: {course.duration}',
        'button_text': 'Enroll Now',
    })


@login_required
def pay(request, enrollment_id):
    """Ask Safaricom to send an M-Pesa PIN prompt to the learner's phone."""
    # Only the owner of the enrollment can pay for it
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, user=request.user)
    course = enrollment.training

    if course.price == 0:
        messages.info(request, 'This course is free. No payment is needed.')
        return redirect('my_enrollments')

    if enrollment.is_paid:
        messages.info(request, 'This course is already paid for.')
        return redirect('my_enrollments')

    if request.method == 'POST':
        try:
            phone = format_phone(request.POST.get('phone', ''))
            response = stk_push(
                phone=phone,
                amount=course.price,
                account_reference=f'ENR{enrollment.id}',
                description='Course fee',
            )
        except MpesaError as error:
            messages.error(request, str(error))
        else:
            # Save a "pending" payment. The callback (Stage 4) will update it later.
            Payment.objects.create(
                user=request.user,
                enrollment=enrollment,
                phone=phone,
                amount=course.price,
                merchant_request_id=response.get('MerchantRequestID', ''),
                checkout_request_id=response.get('CheckoutRequestID', ''),
            )
            messages.success(request, 'Check your phone and enter your M-Pesa PIN to complete the payment.')
            return redirect('my_enrollments')

    user_profile = Profile.objects.filter(user=request.user).first()
    return render(request, 'home/pay.html', {
        'enrollment': enrollment,
        'course': course,
        'phone': user_profile.phone if user_profile else enrollment.phone,
    })


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


def update_payment(payment, result_code, result_desc, receipt=''):
    """Save the result of a payment. Safaricom's code 0 means paid, 1032 means the customer cancelled."""
    if result_code == 0:
        payment.status = 'success'
        payment.mpesa_receipt = receipt
    elif result_code == 1032:
        payment.status = 'cancelled'
    else:
        payment.status = 'failed'
    payment.result_desc = result_desc[:255]
    payment.save()


@csrf_exempt  # Safaricom is not logged in and cannot send a CSRF token
def mpesa_callback(request, token):
    """Safaricom posts the payment result here after the customer pays, cancels or fails."""
    # Only accept calls that use our secret address
    if not settings.MPESA_CALLBACK_SECRET or token != settings.MPESA_CALLBACK_SECRET:
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Rejected'}, status=403)
    if request.method != 'POST':
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'POST only'}, status=405)

    # Read the message Safaricom sent
    try:
        data = json.loads(request.body)
        callback = data['Body']['stkCallback']
        checkout_id = callback['CheckoutRequestID']
        result_code = int(callback['ResultCode'])
    except (ValueError, KeyError, TypeError):
        return JsonResponse({'ResultCode': 1, 'ResultDesc': 'Bad data'}, status=400)

    # Match it to our payment. Only update payments that are still pending,
    # so the same callback arriving twice cannot change a finished payment.
    payment = Payment.objects.filter(checkout_request_id=checkout_id).first()
    if payment is not None and payment.status == 'pending':
        receipt = ''
        description = callback.get('ResultDesc', '')

        if result_code == 0:
            items = callback.get('CallbackMetadata', {}).get('Item', [])
            values = {item.get('Name'): item.get('Value') for item in items}
            receipt = str(values.get('MpesaReceiptNumber', ''))

            # Safety check: the amount paid must match the amount we asked for
            if float(values.get('Amount', 0)) != float(payment.amount):
                result_code = 1
                description = 'Amount paid did not match the course fee.'

        update_payment(payment, result_code, description, receipt)

    # Always answer Safaricom with "accepted"
    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})


@login_required
def check_payment(request, payment_id):
    """The learner clicks 'Check status'. We ask Safaricom what happened to the payment."""
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)

    if request.method == 'POST' and payment.status == 'pending':
        try:
            result = stk_query(payment.checkout_request_id)
        except MpesaError as error:
            messages.info(request, str(error))
        else:
            update_payment(payment, int(result['ResultCode']), result.get('ResultDesc', ''))
            if payment.status == 'success':
                messages.success(request, 'Payment received. Thank you!')
            else:
                messages.warning(request, f'The payment did not go through: {payment.result_desc}')

    return redirect('my_enrollments')