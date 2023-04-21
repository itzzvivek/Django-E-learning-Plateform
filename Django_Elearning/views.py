from django.shortcuts import redirect,render
from core.models import Categories,Course,Level

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status = 'PUBLISH').order_by('-id')
    context={
        'category':category,
        'course':course
    }
    return render(request,'main/home.html', context)

def Single_Course(request):
    category = Categories.get_all_category(Categories)
    level = Level.objects.all()
    course = Course.objects.all()
    context={
        'category':category,
        'level':level,
        'course':course
    }
    return render(request,'main/single_course.html', context)

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')
 
