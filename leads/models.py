from django.db import models
from django.contrib.auth.models import User

class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[('new','New'),('contacted','Contacted'),('done','Done')],
        default='new'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"