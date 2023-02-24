from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from .models import Course
# Create your views here.

class OwnerMixin(object):
    def get_queryset(self):
        qs =super().get_queryset()
        return qs.filter(owner=self.request.user)
    
class OwnerEditMixin(object):
    def form_valid(self,form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerCourseEditMixin):
    template_name = "core/manage/course/form.html"

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'core/manage/course/list.html'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass

class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    pass
