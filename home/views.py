from django.shortcuts import render


def index(request):
    return render(request, 'home/index.html')


def opportunities(request):
    return render(request, 'home/opportunities.html')


def training(request):
    courses = [
        {"title": "Computer Skills", "description": "Learn Microsoft Office, internet use and basic IT skills.", "duration": "4 weeks"},
        {"title": "Web Development", "description": "Build websites with HTML, CSS, JavaScript and Django.", "duration": "12 weeks"},
        {"title": "Entrepreneurship", "description": "Start and grow your own small business.", "duration": "6 weeks"},
        {"title": "CV and Interview Skills", "description": "Write a strong CV and perform well in interviews.", "duration": "2 weeks"},
        {"title": "Digital Marketing", "description": "Learn social media marketing, content and online sales.", "duration": "8 weeks"},
        {"title": "Customer Service", "description": "Communication and service skills for any workplace.", "duration": "3 weeks"},
    ]
    return render(request, 'home/training.html', {"courses": courses})


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    return render(request, 'home/contact.html')