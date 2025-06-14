from django import template
from jobs.models import Application

register = template.Library()

@register.simple_tag
def has_applied(user, job_posting):
    if not user.is_authenticated or user.role != 'candidate':
        return False
    return Application.objects.filter(candidate=user, job_posting=job_posting).exists()