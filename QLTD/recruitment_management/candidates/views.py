from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from .models import CandidateProfile
from .forms import CandidateProfileForm
from accounts.models import User
from jobs.models import JobPosting, Application
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST

# Create your views here.
def candidate_required(view_func):
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, "role") or request.user.role != "candidate":
            return HttpResponseForbidden("Access denied. You must be a candidate to view this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
class CandidateRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == 'candidate'
    
@method_decorator(login_required, name='dispatch')
class CandidateProfileDetailView(DetailView):
    model = CandidateProfile
    template_name = 'candidates/candidate_profile.html'
    context_object_name = 'profile'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context)
        except CandidateProfile.DoesNotExist:
        
            return redirect('candidates:profile_create')

    def get_object(self, queryset=None):
        return CandidateProfile.objects.get(user=self.request.user)
    
@method_decorator(login_required, name='dispatch')
class CandidateProfileUpdateView(UpdateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_profile_edit.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        return get_object_or_404(CandidateProfile, user=self.request.user)
    def get_success_url(self):
        return reverse_lazy('candidates:profile')

@method_decorator(login_required, name='dispatch')
class CandidateProfileCreateView(CreateView):
    model = CandidateProfile
    form_class = CandidateProfileForm
    template_name = 'candidates/candidate_profile_form.html'
    success_url = reverse_lazy('candidates:profile')

    def form_valid(self, form):
        if CandidateProfile.objects.filter(user=self.request.user).exists():
            form.add_error(self.request, "You already have a profile.")
            return self.form_invalid(form)
        form.instance.user = self.request.user
        return super().form_valid(form)
    
@method_decorator(login_required, name='dispatch')
class CandidateProfileDeleteView(DeleteView):
    model = CandidateProfile
    template_name = 'candidates/candidate_profile_confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return get_object_or_404(CandidateProfile, user=self.request.user)
    
class JobSearchListView(ListView):
    model = JobPosting
    template_name = 'candidates/job_search_results.html'
    context_object_name = 'job_postings'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True).order_by('-created_at')
        query = self.request.GET.get('q')
        location = self.request.GET.get('location')
        job_type = self.request.GET.get('job_type')
        category = self.request.GET.get('category')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) | 
                Q(requirements__icontains=query)
            )
        if location:
            queryset = queryset.filter(location__icontains=location)
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if category:
            queryset = queryset.filter(category__icontains=category)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['location'] = self.request.GET.get('location', '')
        context['job_type'] = self.request.GET.get('job_type', '')
        context['category'] = self.request.GET.get('category', '')
        return context
class CandidateApplicationListView(CandidateRequiredMixin, ListView):
    model = Application
    template_name = 'candidates/my_applications.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user).order_by('-applied_at')
    
@candidate_required
def suggested_jobs_view(request):
    suggested_postings = JobPosting.objects.none()

    try: 
        profile = CandidateProfile.objects.get(user=request.user)
        if profile.skills:
            keywords = [s.strip() for s in profile.skills.split(',')]
            for keyword in keywords:
                suggested_postings |= JobPosting.objects.filter(
                    Q(title__icontains=keyword) | 
                    Q(description__icontains=keyword) | 
                    Q(requirements__icontains=keyword)
                ).filter(is_active=True)
            if profile.experience:
                keywords = [s.strip() for s in profile.experience.split(',')]
                for keyword in keywords:
                    suggested_postings |= JobPosting.objects.filter(
                        Q(title__icontains=keyword) | 
                        Q(description__icontains=keyword) | 
                        Q(requirements__icontains=keyword)
                    ).filter(is_active=True)
            
            applied_job_ids =Application.objects.filter(candidate=request.user).values_list('job_posting_id', flat=True)
            suggested_postings = suggested_postings.exclude(id__in=applied_job_ids).distinct()
    except CandidateProfile.DoesNotExist:
        pass
    return render(request, 'candidates/suggested_jobs.html', {'suggested_postings': suggested_postings})

class CandidateDashboardView(CandidateRequiredMixin, DetailView):
    model = CandidateProfile
    template_name = 'candidates/candidate_dashboard.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        try:
            return CandidateProfile.objects.get(user=self.request.user)
        except CandidateProfile.DoesNotExist:
            return None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object:
            context['my_applications_count'] = Application.objects.filter(candidate=self.request.user).count()
        context['suggested_jobs_link'] = reverse_lazy('candidates:suggested_jobs')
        return context

@require_POST
@login_required
def update_avatar(request):
    profile = CandidateProfile.objects.get(user=request.user)
    avatar = request.FILES.get('avatar')
    if avatar:
        profile.avatar = avatar
        profile.save()
    return redirect('candidates:profile')