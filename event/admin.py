from django.contrib import admin
from .models import Category, Conference

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Category, CategoryAdmin)


class ConferenceAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'seat', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'seat', 'available']
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(Conference, ConferenceAdmin)
