from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import CandidateSignUpForm, RecruiterSignUpForm
from .models import User
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.role == 'recruiter':
                return reverse_lazy('accounts:recruiter_home')
            elif self.request.user.role == 'candidate':
                return reverse_lazy('accounts:candidate_home')
            return reverse_lazy('home')
        return super().get_success_url()
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('accounts:login')

class CandidateRegisterView(CreateView):
    model = User
    form_class = CandidateSignUpForm
    template_name = 'accounts/register_candidate.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
    
class RecruiterRegisterView(CreateView):
    model = User
    form_class = RecruiterSignUpForm
    template_name = 'accounts/register_recruiter.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response

@method_decorator(login_required, name='dispatch')
class UserProfileDetailView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user
    
@method_decorator(login_required, name='dispatch')
class UserProfileUpdateView(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email']
    template_name = 'accounts/user_profile_edit.html'
    context_object_name = 'user_profile'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy('accounts:profile')

def recruiter_home(request):
    return render(request, 'accounts/recruiter_home.html')

def candidate_home(request):
    return render(request, 'accounts/candidate_home.html')