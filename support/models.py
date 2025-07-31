from django.db import models
class SupportMessage(models.Model):
    user_id = models.CharField(max_length=100)
    sender = models.CharField(max_length=10, choices=(('user', 'User'), ('admin', 'Admin')))
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='support_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user_id} - {self.sender} - {self.message[:20]}"


