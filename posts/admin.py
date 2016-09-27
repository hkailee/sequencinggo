from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'user', 'created', 'image']
    list_filter = ['created', 'user']
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('user',)
    date_hierarchy = 'created'
    ordering = ['created']
    
admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('body',)
admin.site.register(Comment, CommentAdmin)