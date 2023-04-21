from django.shortcuts import redirect,render
from core.models import Categories,Course,Level
from django.template.loader import render_to_string
from django.http import JsonResponse

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

def filter_data(request):
    categories = request.GET.getlist('category[]')
    level = request.GET.getlist('level[]')
    price = request.GET.getlist('price[]')
    print(price)


    if price == ['pricefree']:
       course = Course.objects.filter(price=0)
    elif price == ['pricepaid']:
       course = Course.objects.filter(price__gte=1)
    elif price == ['priceall']:
       course = Course.objects.all()
    elif categories:
       course = Course.objects.filter(category__id__in=categories).order_by('-id')
    elif level:
       course = Course.objects.filter(level__id__in = level).order_by('-id')
    else:
       course = Course.objects.all().order_by('-id')


    t = render_to_string('ajax/course.html',{'course': course})
    return JsonResponse({'data':t})

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')
 
