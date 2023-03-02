from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from .models import Course
from django.views.generic.base import TemplateResponseMixin,View
from django.forms.models import modelform_factory
from django.apps import apps
from .models import Module, Content
from .forms import ModuleFormSet
from django.db.models import Count
from .models import Subject
from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.views.generic.detail import DetailView

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
    template_name = 'core/manage/module/formset.html'
    course = None
    
    def get_formset(self,data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self,request,pk):
        self.course = get_object_or_404(Course,id=pk,owner=request.user)
        return super().dispatch(request,pk)
    
    def get(self, request, *args, **kwargs):
        formset = self.get_formset()
        return self.render_to_response({'course':self.course,'formset':formset})
    
    def post(self,request,*args,**kwargs):
        formset = self.get_formset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect('manage_course_list')
        return self.render_to_response({'course':self.course,'formset':formset})


class ContentCreateUpdateView(TemplateResponseMixin, View):
    module = None
    model = None
    obj = None
    template_name = 'core/manage/content/form.html'

    def get_model(self,model_name):
        if model_name in ['text','video','image','file']:
            return apps.get_model(app_label='courses',model_name=model_name)
        return None

    def get_form(self,model, *args,**kwargs):
        Form = modelform_factory(model, exclude=['owner','order','created','updated'])
        return Form(*args,**kwargs)
    
    def dispatch(self, request, module_id, model_name, id=None):
        self.module = get_object_or_404(Module,
                                         id=module_id,
                                         course__owner = request.user)
        self.model = self.get_model(model_name)
        if id:
            self.obj = get_object_or_404(self.model,
                                         id=id,
                                         owner=request.user)
        return super.dispatch(request, module_id,model_name = id)
    
    def get(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({'form':form,
                                       'object':self.obj})
    def post(self,request,module_id,model_name,id=None):
        form = self.get_form(self.model, instance=self.obj,
                             data=request.POST,files=request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not id:
                #new content
                Content.objects.create(module=self.module,item=obj)
            return redirect('module_content_list',self.module.id)
        return self.render_to_response({'form':form,'object':self.obj})

class ContentDeleteView(View):
    def post(self,request,id):
        content = get_object_or_404(Content,id=id,module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list',module.id)

class moduleContentListView(TemplateResponseMixin, View):
    template_name = 'core/manage/module/content_list.html'

    def get(self, request,module_id):
        module = get_object_or_404(Module,
        id=module_id,
        course__owner=request.user)
    
        return self.render_to_response({'module': module})

class ModuleOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self,request):
        for id,order in self.request_json.item():
            module.objects.filter(id=id,course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class ContentOrderView(CsrfExemptMixin,JsonRequestResponseMixin,View):
    def post(self,request):
        for id, order in self.request_json.item():
            Content.objects.filter(id=id, module__course__owner=request.user).update(order=order)
        return self.render_json_response({'saved': 'OK'})

class CourseListView(TemplateResponseMixin,View):
    model = Course
    template_name = 'core/course/list.html'

    def get(self,request,subject=None):
        subjects = Subject.objects.annotate(
                    total_courses = Count('courses'))
        courses = Course.objects.annotate(
                total_modules = Count('modules'))
        
        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)
        return self.render_to_response({
            'subjects':subjects,'subject':subject,'courses':courses})

class CourseDetailView(DetailView):
    model = Course
    template_name = 'core/course/detail.html'