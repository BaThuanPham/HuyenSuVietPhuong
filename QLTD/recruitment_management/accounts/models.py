from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    USER_ROLES = [
        ('admin', 'Admin'),
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
    ]
    role = models.CharField(max_length=20, choices=USER_ROLES, default='candidate')

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='accounts_users',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='accounts_users',
    )

    def __str__(self):
        return self.username
    
class RecruiterProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, limit_choices_to={'role': 'recruiter'})
    company_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    company_address = models.CharField(max_length=255)
    company_website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name