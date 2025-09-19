from django.contrib import admin, messages
from django.db import transaction

from .models import Bio, Project, Resume

@admin.register(Bio)
class BioAdmin(admin.ModelAdmin):
    list_display = ("name", "email")

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at")
    search_fields = ("title",)

@admin.action(description="Make selected resume active (deactivates all others)")
def make_active_resume(modeladmin, request, queryset):
    count = queryset.count()
    if count != 1:
        messages.error(request, "Select exactly one resume for this action.")
        return
    
    obj = queryset.first()
    with transaction.atomic():
        # First set all to inactive to avoid the unique-constraint clash
        Resume.objects.update(is_active=False)
        obj.is_active = True
        obj.save(update_fields=["is_active"])
    
    messages.success(request, f"'{obj}' is now the active resume.")

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("uploaded_at", "is_active", "file")
    list_filter = ("is_active", "uploaded_at")
    ordering = ("-uploaded_at",)
    actions = [make_active_resume]
