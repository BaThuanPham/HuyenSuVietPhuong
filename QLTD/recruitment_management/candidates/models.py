from django.db import models
from accounts.models import User
# Create your models here.

class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE, primary_key=True, limit_choices_to={'role': 'candidate'})
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    cv_file = models.FileField(upload_to='cv_files/', blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    def __str__(self):
        return self.full_name