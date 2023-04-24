"""Django_Elearning URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from . import views,user_login

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.HOME,name='home'),
    path('base',views.BASE,name='base'),
    path('courses',views.Single_Course,name='single_course'),
    path('course/<slug:slug>',views.Course_details,name = 'course_details'),
    path('product/filter-data',views.filter_data,name='filter-data'),
    path('search',views.search_course,name='search_course'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('account/register',user_login.register,name='register'),
    path('account/',include('django.contrib.auth.urls')),
    path('login',user_login.login,name='login'),
    
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
