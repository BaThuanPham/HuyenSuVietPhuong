from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'candidates'

urlpatterns = [
    path('profile/', views.CandidateProfileDetailView.as_view(), name='profile'),
    path('profile/edit/', views.CandidateProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/create/', views.CandidateProfileCreateView.as_view(), name='profile_create'),
    path('profile/delete/', views.CandidateProfileDeleteView.as_view(), name='profile_delete'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='change_password'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('dashboard/', views.CandidateDashboardView.as_view(), name='candidate_dashboard'),
    path('my-applications/', views.CandidateApplicationListView.as_view(), name='my_applications'),
    path('suggested-jobs/', views.suggested_jobs_view, name='suggested_jobs'),
    path('profile/update-avatar/', views.update_avatar, name='update_avatar'),
    path('search/', views.JobSearchListView.as_view(), name='job_search'),
]