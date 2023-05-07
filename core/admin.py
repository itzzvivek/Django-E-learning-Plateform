from django.contrib import admin
from .models import Categories,Author,Course,Level,What_you_learn,Requirements

# Register your models here.

class What_you_learn_TabularInline(admin.TabularInline):
    model = What_you_learn

class Requirements_TabularInline(admin.TabularInline):
    model = Requirements

class course_admin(admin.ModelAdmin):
    inlines = (What_you_learn_TabularInline,Requirements_TabularInline)

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(What_you_learn)
admin.site.register(Requirements)