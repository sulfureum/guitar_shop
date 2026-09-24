from django.contrib import admin
from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['created_at']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'price', 'created_at']
    list_display_links = ['id', 'name']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ['id', 'fullname', 'email', 'created_at']
    list_display_links = ['id', 'fullname']
    list_filter = ['created_at']
    search_fields = ['first_name', 'lastname', 'message']

    @admin.display()
    def fullname(self, instance):
        return f'{instance.first_name} {instance.lastname}'

    fullname.short_description = 'First name and Lastname'


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']
    list_display_links = ['id', 'user']
    list_filter = ['created_at', 'product']
    search_fields = ('user__username', 'text')


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.HomeSlider)


