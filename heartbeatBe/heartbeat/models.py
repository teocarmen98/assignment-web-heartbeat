from django.db import models

# Create your models here.
class UrlItem(models.Model):
    url = models.CharField(max_length=255, unique=True)
    status = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url