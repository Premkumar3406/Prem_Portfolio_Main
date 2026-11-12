from django.db import models

class Home(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='home_images/')

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=150, default='General Inquiry')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class Resume(models.Model):
    title = models.CharField(max_length=150, default="Prem Kumar Resume")
    file = models.FileField(upload_to='files/')
    uploaded_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, help_text="Mark active to serve this resume on the portfolio")

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Resume'
        verbose_name_plural = 'Resumes'

    def __str__(self):
        return f"{self.title} ({self.uploaded_at.strftime('%Y-%m-%d')})"


class Project(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=200, help_text="e.g. Machine Learning · XGBoost · SHAP · LIME")
    short_tag = models.CharField(max_length=100, blank=True, help_text="e.g. ML · Explainable AI")
    description = models.TextField(help_text="Detailed project summary shown in the details card")
    image = models.ImageField(upload_to='projects/', blank=True, null=True, help_text="Cover screenshot / image")
    live_demo_url = models.URLField(blank=True, null=True, help_text="Live demo URL (e.g. https://myproject.com)")
    github_url = models.URLField(blank=True, null=True, help_text="GitHub repository URL")
    order = models.PositiveIntegerField(default=0, help_text="Display order (0 = first, 1 = second, etc.)")
    is_active = models.BooleanField(default=True, help_text="Keep checked to display on website")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Project'
        verbose_name_plural = 'Projects'

    def __str__(self):
        return self.title
