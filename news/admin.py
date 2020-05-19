from django.contrib import admin
from .models import News, Tag, Category

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Tag)

