from django.shortcuts import redirect,render
from core.models import Categories

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    context={
        'category':category
    }
    return render(request,'main/home.html', context)

def Single_Course(request):
    return render(request,'main/single_course.html')

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')

