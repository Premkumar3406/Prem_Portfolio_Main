from django.contrib import admin
from .models import Home, ContactMessage, Resume, Project

@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'image')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'is_active', 'uploaded_at')
    list_filter = ('is_active', 'uploaded_at')
    search_fields = ('title',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_tag', 'live_demo_url', 'order', 'is_active', 'created_at')
    list_editable = ('order', 'is_active')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'category', 'description')