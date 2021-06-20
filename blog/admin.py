from django.contrib import admin

from .models import Blog

class Blogadmin(admin.ModelAdmin):
    class Meta:
        model = Blog

admin.site.register(Blog,Blogadmin)


