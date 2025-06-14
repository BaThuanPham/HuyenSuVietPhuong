from django.urls import path, include
from . import views
app_name = 'jobs'

urlpatterns = [
    path('list/', views.JobPostingListView.as_view(), name='job_list'),
    path('<int:pk>/', views.JobPostingDetailView.as_view(), name='job_detail'),
    path('create/', views.JobPostingCreateView.as_view(), name='job_create'),
    path('<int:pk>/edit/', views.JobPostingUpdateView.as_view(), name='job_edit'),
    path('<int:pk>/delete/', views.JobPostingDeleteView.as_view(), name='job_delete'),

    path('dashboard/recruiter/', views.RecruiterDashboardView.as_view(), name='recruiter_dashboard'),
    path('my-postings/', views.RecruiterDashboardView.as_view(), name='my_job_postings'),

    path('<int:pk>/apply/', views.ApplyForJobView.as_view(), name='apply_job'),


    path('applications/', views.ApllicationListView.as_view(), name='application_list'),
    path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),

    
    path('applications/<int:application_pk>/interview/create/', views.InterviewCreateView.as_view(), name='interview_create'),
    path('interview/<int:pk>/edit/', views.InterviewUpdateView.as_view(), name='interview_edit'),

   
    path('applications/<int:application_pk>/test/create/', views.TestCreateView.as_view(), name='test_create'),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),

]