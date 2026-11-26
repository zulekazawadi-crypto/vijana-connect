from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='index'),
    path('opportunities/', views.opportunities, name='opportunities'),
    path('training/', views.training, name='training'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Apply and enroll (the number in the address is the item's id)
    path('apply/<int:opp_id>/', views.apply, name='apply'),
    path('enroll/<int:course_id>/', views.enroll, name='enroll'),

    # Payment for a training course
    path('pay/<int:enrollment_id>/', views.pay, name='pay'),
    path('payments/check/<int:payment_id>/', views.check_payment, name='check_payment'),
    path('payments/callback/<str:token>/', views.mpesa_callback, name='mpesa_callback'),

    # Tracking
    path('my-applications/', views.my_applications, name='my_applications'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),

    # Accounts and profile
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]