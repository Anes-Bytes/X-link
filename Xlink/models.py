from django.db import models
from django.contrib.auth import get_user_model


class CardTemplate(models.Model):
    CATEGORY_CHOICES = (
        ('minimal', 'Minimal'),
        ('dark', 'Dark / Cyber'),
        ('neon', 'Neon / Futuristic'),
        ('corporate', 'Professional / Corporate'),
        ('gradient', 'Gradient'),
        ('creative', 'Creative / Modern'),
    )

    template_id = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES)
    description = models.CharField(max_length=255)
    preview_image = models.ImageField(upload_to='templates_images', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.template_id})"

    def to_dict(self):
        return {
            "templateId": self.template_id,
            "name": self.name,
            "category": self.category,
            "categoryLabel": self.get_category_display(),
            "visualStyle": self.visual_style,
            "description": self.description,
            "previewImage": self.preview_image,
            "styleTag": self.style_tag,
            "customizationOptions": self.customization_options or {},
        }


class TemplateSelection(models.Model):
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='template_selections',
    )
    session_id = models.CharField(max_length=64, blank=True, db_index=True)
    template = models.ForeignKey(
        CardTemplate,
        on_delete=models.CASCADE,
        related_name='selections'
    )
    customization_payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        owner = self.user.email if self.user else self.session_id or 'anonymous'
        return f"{owner} -> {self.template.template_id}"
