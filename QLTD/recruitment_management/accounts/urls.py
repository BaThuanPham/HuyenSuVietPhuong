from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'

urlpatterns= [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/candidate/', views.CandidateRegisterView.as_view(), name='register_candidate'),
    path('register/recruiter/', views.RecruiterRegisterView.as_view(), name='register_recruiter'),
    path('profile/', views.UserProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.UserProfileUpdateView.as_view(), name='profile_edit'),
    path('recruiter/home/', views.recruiter_home, name='recruiter_home'),
    path('candidate/home/', views.candidate_home, name='candidate_home'),
]