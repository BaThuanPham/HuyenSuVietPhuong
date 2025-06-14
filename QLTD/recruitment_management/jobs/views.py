from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import JobPosting, Application, Interview, Test
from .forms import JobPostingForm, ApplicationForm, InterviewForm, TestForm
from accounts.models import User

# Create your views here.

class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'recruiter'
    
class CandidateRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'candidate'

class JobPostingListView(ListView):
    model = JobPosting
    template_name ='jobs/job_listing.html'
    context_object_name = 'job_postings'
    queryset = JobPosting.objects.filter(is_active=True).order_by('-created_at')

class JobPostingDetailView(DetailView):
    model = JobPosting
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job_posting'

class JobPostingCreateView(RecruiterRequiredMixin, CreateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'jobs/job_form.html'
    success_url = reverse_lazy('jobs:my_job_postings')

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)

class JobPostingUpdateView(RecruiterRequiredMixin, UpdateView):
    model = JobPosting
    form_class = JobPostingForm
    template_name = 'jobs/job_form.html'
    context_object_name = 'job_posting'

    def get_queryset(self):
        return reverse_lazy('jobs:job_detail', kwargs={'pk': self.object.pk})
    
class JobPostingDeleteView(RecruiterRequiredMixin, DeleteView):
    model = JobPosting
    template_name = 'jobs/job_confirm_delete.html'
    success_url = reverse_lazy('jobs:my_job_postings')

    def get_queryset(self):
        return JobPosting.objects.filter(posted_by=self.request.user)

class RecruiterDashboardView(RecruiterRequiredMixin, ListView):
    model = JobPosting
    template_name = 'jobs/recruiter_dashboard.html'
    context_object_name = 'job_postings'

    def get_queryset(self):
        return JobPosting.objects.filter(posted_by=self.request.user).order_by('-created_at')
    
class ApplyForJobView(CandidateRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'jobs/apply_confirm.html'
    success_url = reverse_lazy('candidates:my_applications')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_posting = get_object_or_404(JobPosting, pk=self.kwargs.get('pk'))
        context['job_posting'] = job_posting
        return context

    def form_valid(self, form):
        job_posting_id = self.kwargs.get('pk')
        job_posting = get_object_or_404(JobPosting, pk=job_posting_id)

        if Application.objects.filter(job_posting=job_posting, candidate=self.request.user).exists():
            form.add_error(None, "You have already applied for this job.")
            return self.form_invalid(form)
        
        form.instance.job_posting = job_posting
        form.instance.candidate = self.request.user
        response = super().form_valid(form)

class ApllicationListView(CandidateRequiredMixin, ListView):
    model = Application
    template_name = 'jobs/application_list.html'
    context_object_name = 'applications'

    def get_queryset(self):
        if self.request.user.role == 'recruiter':
            return Application.objects.filter(job_posting__posted_by=self.request.user).order_by('-applied_at')
        return Application.objects.all().order_by('-applied_at')

class ApplicationDetailView(CandidateRequiredMixin, DetailView):
    model = Application
    template_name = 'jobs/application_detail.html'
    context_object_name = 'application'

    def get_queryset(self):
        user = self.request.user
        if user.role == 'recruiter':
            return Application.objects.filter(job_posting__posted_by=user)
        elif user.role == 'candidate':
            return Application.objects.filter(candidate=user)
        return Application.objects.none() 

class InterviewCreateView(RecruiterRequiredMixin, CreateView):
    model = Interview
    form_class = InterviewForm
    template_name = 'jobs/interview_form.html'

    def get_success_url(self):
        return reverse_lazy('jobs:application_detail', kwargs={'pk': self.object.application.pk})
    
    def form_valid(self, form):
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, pk=application_id)
        form.instance.application = application
        form.instance.interviewer = self.request.user
        return super().form_valid(form)

class InterviewUpdateView(RecruiterRequiredMixin, UpdateView):
    model = Interview
    form_class = InterviewForm
    template_name = 'jobs/interview_form.html'

    def get_queryset(self):
        return Interview.objects.filter(application__job_posting__posted_by=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('jobs:application_detail', kwargs={'pk': self.object.application.pk})
    
class TestCreateView(RecruiterRequiredMixin, CreateView):
    model = Test
    form_class = TestForm
    template_name = 'jobs/test_form.html'

    def get_success_url(self):
        return reverse_lazy('jobs:application_detail', kwargs={'pk': self.object.application.pk})
    
    def form_valid(self, form):
        application_id = self.kwargs.get('application_pk')
        application = get_object_or_404(Application, pk=application_id)
        form.instance.application = application
        return super().form_valid(form)