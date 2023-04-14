from django.shortcuts import redirect,render

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    return render(request,'main/home.html')

def Single_Course(request):
    return render(request,'main/single_course.html')

def about(request):
    return render(request,'main/about.html')

def contact(request):
    return render(request,'main/contact.html')

