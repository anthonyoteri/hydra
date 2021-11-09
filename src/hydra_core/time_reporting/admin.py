from django.contrib import admin

from .models import Category, Project, SubProject, TimeRecord

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(SubProject)
admin.site.register(TimeRecord)
