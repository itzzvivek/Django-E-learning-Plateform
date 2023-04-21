from django.contrib import admin
from .models import Categories,Author,Course,Level

# Register your models here.

admin.site.register(Categories)
admin.site.register(Author)
admin.site.register(Course)
admin.site.register(Level)