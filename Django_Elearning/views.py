from django.shortcuts import redirect,render
from core.models import Categories,Course,Level,UserCourse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Sum

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
    freecourse_count = Course.objects.filter(price=0).count()
    paidcourse_count = Course.objects.filter(price__gte=1).count()
    context={
        'category':category,
        'level':level,
        'course':course,
        'freecourse_count':freecourse_count,
        'paidcourse_count': paidcourse_count
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
    category = Categories.get_all_category(Categories)
    context={
        'category':category
    }
    return render(request,'main/about.html', context)

def contact(request):
    category = Categories.get_all_category(Categories)
    context = {
        'category':category
    }
    return render(request,'main/contact.html',context)
 
def search_course(request):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains=query)
    category = Categories.get_all_category(Categories)

    context={
        'course':course,
        'category':category
    }

    return render(request,'search/search.html',context)

def Course_details(request,slug):
    category = Categories.get_all_category(Categories)
    time_duration = Video.objects.filter(course_slug=slug).aggregate(sum=Sum('time_duration'))
    course_id = Course.objects.get(slug=slug)
    try:
        check_enroll = UserCourse.objects.get(user = request.user, course=course_id )
    except UserCourse.DoesNotExist:
        check_enroll = None
    course = Course.objects.filter(slug=slug)
    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context={
        'course':course,
        'category':category,
        'time_duration': time_duration,
        'check_enroll':check_enroll
    }
    return render(request,'course/course_details.html',context)

def page_not_found(request):
    category = Categories.get_all_category(Categories)
    context={
        'category':category
    }
    return render(request,'error/404.html', context)

def checkout(request,slug):
    course = Course.objects.get(slug=slug)
    if course.price==0:
        course = UserCourse(
            user = request.user,
            course = course,
        )
        course.save()
        return redirect('home')
    return render(request,'checkout/checkout.html')