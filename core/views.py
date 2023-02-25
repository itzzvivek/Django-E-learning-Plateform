from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
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

class OwnerCourseMixin(OwnerMixin,LoginRequiredMixin,PermissionRequiredMixin):
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin,OwnerEditMixin):
    template_name = "core/manage/course/form.html"

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'core/manage/course/list.html'
    permission_required = 'core.view_course'

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'core.change_course'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'core.add_course'

class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    template_name = 'core/manage/course/delete.html'
    permission_required = 'core.delete_course'














