from django.db import models
from django.db.models import Q


class Bio(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    email = models.EmailField()
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)

    @property
    def first_name(self):
        return self.name.split()[0] if self.name else ""

    def __str__(self):
        return self.name


class Skill(models.Model):
    class Category(models.TextChoices):
        BACKEND = "backend", "Backend"
        FRONTEND = "frontend", "Frontend"
        DEVOPS = "devops", "DevOps"
        DATA = "data", "Data"
        TOOLS = "tools", "Tools/Other"
    
    name = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=20, choices=Category.choices, blank=True)
    level = models.PositiveSmallIntegerField(default=3)
    priority = models.PositiveSmallIntegerField(default=0)  # controls display order
    pinned = models.BooleanField(default=True)              # controls visibility

    class Meta:
        ordering = ["priority", "name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/', null=True, blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Resume(models.Model):
    file = models.FileField(upload_to="resumes/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["is_active"],
                condition=Q(is_active=True),  # enforce when is_active is True
                name="only_one_active_resume",
            )
        ]
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_active:
            # Deactivate any other active resumes before saving this one
            (Resume.objects
            .exclude(pk=self.pk)
            .filter(is_active=True)
            .update(is_active=False))

    def __str__(self):
        return f"Resume ({self.uploaded_at:%Y-%m-%d})"
