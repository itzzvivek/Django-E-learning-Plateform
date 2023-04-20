from django.contrib import admin
from .models import Categories,Author,Course

# Register your models here.

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course)