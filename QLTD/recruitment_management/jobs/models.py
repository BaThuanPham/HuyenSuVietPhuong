from django.db import models
from accounts.models import User

# Create your models here.
class JobPosting(models.Model):
    JOB_TYPES=(
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('Freelance', 'Freelance'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'candidate'})
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='applied')

    def __str__(self):
        return f"Application for {self.job_posting.title} by {self.candidate.username}"

class Interview(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'recruiter'})
    scheduled_time = models.DateTimeField()
    round_number = models.IntegerField(default=1)
    status = models.CharField(max_length=50, default='scheduled')
    notes = models.TextField(blank=True, null=True)

class Test(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    test_url = models.URLField(blank=True, null=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()