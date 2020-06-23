from django.contrib import admin


from .models import Post, Tag, Category, Comment
from django_summernote.admin import SummernoteModelAdmin


class NewsModelAdmin(SummernoteModelAdmin, admin.ModelAdmin):  # instead of ModelAdmin
    summernote_fields = ['description', 'text']
    search_fields = ['title']
    list_display = ('title', 'is_approved', 'is_editing_approved')
    list_filter = ['is_approved', 'is_editing_approved']

    def get_ordering(self, request):
        return ['is_approved', 'is_editing_approved']



admin.site.register(Post, NewsModelAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Comment)

