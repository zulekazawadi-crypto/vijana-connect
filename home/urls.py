from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('opportunities/', views.opportunities, name='opportunities'),
    path('training/', views.training, name='training'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]