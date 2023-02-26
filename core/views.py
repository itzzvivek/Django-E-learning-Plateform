from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic.base import TemplateResponseMixin, View
from .forms import  ModuleFormSet
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

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'core/manage/course/delete.html'
    permission_required = 'core.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'core/manage/course/module/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course,data=data)
    
    def dispatch(self,request,pk):
        self.course = get_object_or_404(Course,id=pk,owner=request.user)
        return super().dispatch(request, pk)
    
    def get(self,request,*args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course,
                                        'formset':formset})
    
    def post(self,request,*args, **kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course,   'formset':formset})











