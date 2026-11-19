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

    # Accounts
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]